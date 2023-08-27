from repository.repositories import UserRepository
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Form,
    Security,
    BackgroundTasks,
    Request,
)
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import User
from services.auth_manager import auth_manager
from services.email import send_email
from api.schemas.users import UserCreate, TokenModel, UserResponse, RequestEmail


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    exist_user = user_repository.get_user_by_email(user.email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    user.password = auth_manager.get_password_hash(user.password)
    new_user = user_repository.create_user(user)
    background_tasks.add_task(send_email, new_user.email, request.base_url)
    return {"user": new_user, "detail": "User successfully created"}


@router.post("/login", response_model=TokenModel)
def login(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed"
        )
    if not auth_manager.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    # Generate JWT
    access_token = auth_manager.create_access_token(data={"sub": user.email})
    refresh_token = auth_manager.create_refresh_token(data={"sub": user.email})

    user_repository.update_token(user, refresh_token, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token/")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    user_id = auth_manager.verify_token(refresh_token)
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    access_token = auth_manager.create_access_token({"sub": user_id})
    return {"access_token": access_token}


# @router.get("/confirm-email/{email}")
# def confirm_email(email: str, db: Session = Depends(get_db)):
#     confirmed_email(email, db)
#     return {"message": "Email confirmed successfully"}


@router.get("/confirmed_email/{token}")
def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = auth_manager.get_email_from_token(token)
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    user_repository.confirmed_email(email)
    return {"message": "Email confirmed"}


@router.post("/request_email")
def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(body.email)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, request.base_url)
    return {"message": "Check your email for confirmation."}
