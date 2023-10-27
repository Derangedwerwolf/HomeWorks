from datetime import datetime, timedelta
from database.db import get_db
from sqlalchemy.orm import Session
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database.models import User
from repository.repositories import UserRepository


class AuthManager:
    """
    Manages authentication-related operations.

    Attributes:
        SECRET_KEY (str): Secret key for encoding and decoding JWT tokens.
        ALGORITHM (str): Algorithm used for encoding and decoding JWT tokens.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Expiration time for access tokens in minutes.
        oauth2_scheme (OAuth2PasswordBearer): OAuth2 password bearer scheme for token extraction.
        pwd_context (CryptContext): Password hashing context.
    """

    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """
        Verify a plain password against a hashed password.

        :param plain_password: Plain password to verify.
        :type plain_password: str
        :param hashed_password: Hashed password to compare against.
        :type hashed_password: str
        :return: Whether the password is verified.
        :rtype: bool
        """

        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Generate a hashed password from a plain password.

        :param password: Plain password.
        :type password: str
        :return: Hashed password.
        :rtype: str
        """

        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: int = 30):
        """
        Create an access token.

        :param data: Data to encode in the token.
        :type data: dict
        :param expires_delta: Expiration time for the token in minutes.
        :type expires_delta: int
        :return: Access token.
        :rtype: str
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, data: dict, expires_delta: int = 7):
        """
        Create a refresh token.

        :param data: Data to encode in the token.
        :type data: dict
        :param expires_delta: Expiration time for the token in days.
        :type expires_delta: int
        :return: Refresh token.
        :rtype: str
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=expires_delta)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(
                refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    def verify_token(self, token: str):
        """
        Verify and decode a JWT token.

        :param token: JWT token to verify.
        :type token: str
        :return: Decoded token payload.
        :rtype: dict
        :raises HTTPException: If the token is invalid.
        """

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ):
        """
        Get the current user based on the access token.

        :param token: Access token.
        :type token: str
        :param db: Database session.
        :type db: Session
        :return: Current user.
        :rtype: User
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception

            user_repository = UserRepository(db)
            user = user_repository.get_user_by_email(email)

            if user is None:
                raise credentials_exception
            return user
        except JWTError:
            raise credentials_exception

    def create_email_token(self, data: dict):
        """
        Create an email verification token.

        :param data: Data to encode in the token.
        :type data: dict
        :return: Email verification token.
        :rtype: str
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def get_email_from_token(self, token: str):
        """
        Get the email from an email verification token.

        :param token: Email verification token.
        :type token: str
        :return: Email address.
        :rtype: str
        :raises HTTPException: If the token is invalid.
        """

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )


auth_manager = AuthManager()
