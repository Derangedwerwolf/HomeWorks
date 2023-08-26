from app.repository.repositories import UserRepository
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import User
from app.services.auth_manager import auth_manager
from app.api.schemas.users import UserModel, TokenModel, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(user: UserModel, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    exist_user = user_repository.get_user_by_email(user.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    user.password = auth_manager.get_password_hash(user.password)
    new_user = user_repository.create_user(user, db)
    return {"user": new_user, "detail": "User successfully created"}


@router.post("/login", response_model=TokenModel)
def login(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
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
    user = UserRepository.get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    access_token = auth_manager.create_access_token({"sub": user_id})
    return {"access_token": access_token}
