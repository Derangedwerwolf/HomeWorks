from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Contact(Base):
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
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    confirmed = Column(Boolean, default=False)
    refresh_token = Column(String)
    contacts = relationship("Contact", backref="user")
