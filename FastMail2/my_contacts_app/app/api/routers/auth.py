from repository.repositories import UserRepository
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Security,
    BackgroundTasks,
    Request,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import User
from services.auth_manager import auth_manager
from services.email import send_email
from api.schemas.users import UserCreate, TokenModel, UserResponse, RequestEmail


router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Sign up a new user.

    :param user: User information for sign up.
    :type user: UserCreate
    :param background_tasks: Background tasks manager.
    :type background_tasks: BackgroundTasks
    :param request: HTTP request.
    :type request: Request
    :param db: Database session.
    :type db: Session
    :return: Created user and success message.
    :rtype: UserResponse
    :raises HTTPException: If the user already exists or an error occurs during sign up.
    """

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
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Log in a user and issue an access token.

    :param body: OAuth2 password request form containing username and password.
    :type body: OAuth2PasswordRequestForm
    :param db: Database session.
    :type db: Session
    :return: Token model containing access and refresh tokens.
    :rtype: TokenModel
    :raises HTTPException: If the user is not found or the provided credentials are invalid.
    """

    user_repository = UserRepository(db)
    token = credentials.credentials
    email = auth_manager.decode_refresh_token(token)
    user = user_repository.get_user_by_email(body.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not auth_manager.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    # Generate JWT
    access_token = auth_manager.create_access_token(data={"sub": user.email})
    refresh_token = auth_manager.create_refresh_token(data={"sub": user.email})

    user_repository.update_token(user, refresh_token, db)

    return {
        "username": user.username,  # Add this line
        "email": user.email,  # Add this line
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=TokenModel)
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    """
    Refresh an access token using a refresh token.

    :param credentials: HTTP authorization credentials containing the refresh token.
    :type credentials: HTTPAuthorizationCredentials
    :param db: Database session.
    :type db: Session
    :return: Token model containing updated access and refresh tokens.
    :rtype: TokenModel
    :raises HTTPException: If the refresh token is invalid or an error occurs.
    """

    token = credentials.credentials
    email = auth_manager.decode_refresh_token(token)
    user = UserRepository.get_user_by_email(email, db)
    if user.refresh_token != token:
        UserRepository.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = auth_manager.create_access_token(data={"sub": email})
    refresh_token = auth_manager.create_refresh_token(data={"sub": email})
    UserRepository.update_token(user, refresh_token, db)
    return {
        "username": user.username,  # Add this line
        "email": email,  # Add this line
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/confirmed_email/{token}")
def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    Confirm the user's email using a confirmation token.

    :param token: Email confirmation token.
    :type token: str
    :param db: Database session.
    :type db: Session
    :return: Confirmation message.
    :rtype: dict
    :raises HTTPException: If verification fails or an error occurs.
    """

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
    """
    Request email confirmation.

    :param body: RequestEmail model containing the email.
    :type body: RequestEmail
    :param background_tasks: Background tasks manager.
    :type background_tasks: BackgroundTasks
    :param request: HTTP request.
    :type request: Request
    :param db: Database session.
    :type db: Session
    :return: Confirmation message or email sending status.
    :rtype: dict
    """

    user_repository = UserRepository(db)
    user = user_repository.get_user_by_email(body.email)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, request.base_url)
    return {"message": "Check your email for confirmation."}
