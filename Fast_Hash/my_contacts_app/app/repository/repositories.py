from sqlalchemy.orm import Session
from ..database.models import User
from api.schemas.contact import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = User(email=user.email, hashed_password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def update_token(self, user: User, token: str | None, db: Session) -> None:
        user.refresh_token = token
        db.commit()
