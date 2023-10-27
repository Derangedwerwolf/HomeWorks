# from database.crud import get_user_by_email
from sqlalchemy.orm import Session
from database.models import User
from api.schemas.users import UserCreate
from api.schemas.users import UserDb


class UserRepository:
    """
    Repository class for managing user data.
    """

    def __init__(self, db: Session):
        """
        Initialize the UserRepository.

        :param db: Database session.
        :type db: Session
        """
        self.db = db

    def create_user(self, user: UserCreate) -> UserDb:
        """
        Create a new user.

        :param user: User data.
        :type user: UserCreate
        :return: Created user.
        :rtype: UserDb
        """
        db_user = User(email=user.email, hashed_password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        # Construct a UserDb instance with the appropriate attributes
        created_user = UserDb(
            id=db_user.id,
            username=user.username,
            email=user.email,
            avatar=None,  # Set the avatar if applicable
        )

        return created_user

    def get_user_by_email(self, email: str):
        """
        Retrieve a user by email.

        :param email: User's email.
        :type email: str
        :return: User with the given email.
        :rtype: User or None
        """
        return self.db.query(User).filter(User.email == email).first()

    def update_token(self, user: User, token: str | None, db: Session) -> None:
        """
        Update a user's refresh token.

        :param user: User to update.
        :type user: User
        :param token: Refresh token.
        :type token: str or None
        :param db: Database session.
        :type db: Session
        """
        user.refresh_token = token
        db.commit()

    def confirmed_email(self, email: str) -> None:
        """
        Mark a user's email as confirmed.

        :param email: User's email.
        :type email: str
        """
        user = self.get_user_by_email(email)
        user.confirmed = True
        self.db.commit()
