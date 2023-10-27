from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Contact(Base):
    """
    Database model representing a contact.

    Attributes:
        id (int): Contact's unique identifier.
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Email address of the contact.
        phone_number (str): Phone number of the contact.
        birthday (Date): Birthday of the contact.
        avatar (str): URL to the contact's avatar image.
        additional_data (str): Additional data about the contact.
        user_id (int): ID of the associated user.
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    avatar = Column(String(255), nullable=True)
    additional_data = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), default=None)
    # refresh_token = Column(String(255), nullable=True)


class User(Base):
    """
    Database model representing a user.

    Attributes:
        id (int): User's unique identifier.
        email (str): Email address of the user.
        hashed_password (str): Hashed password of the user.
        confirmed (bool): Indicates if the user's email is confirmed.
        refresh_token (str): Refresh token for the user's authentication.
        contacts (relationship): Relationship to the user's contacts.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    confirmed = Column(Boolean, default=False)
    refresh_token = Column(String)
    contacts = relationship("Contact", backref="user")
