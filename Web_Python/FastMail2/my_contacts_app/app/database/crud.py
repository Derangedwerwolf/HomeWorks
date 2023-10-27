import logging

from sqlalchemy import and_
from sqlalchemy.orm import Session
from .models import Contact
from api.schemas.contact import ContactCreate, ContactUpdate
from database.models import User
from datetime import date
from typing import List

logger = logging.getLogger(__name__)


def create_contact(db: Session, user_id: int, contact: ContactCreate):
    try:
        logger.info(f"Creating a new contact in the database: {contact}")
        # contact_dict = contact.dict()  # Convert ContactCreate to a dictionary
        # db_contact = Contact(**contact.dict())
        contact["user_id"] = user_id
        db_contact = Contact(**contact.model_dump())
        print(db_contact)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except Exception as e:
        logger.error(f"Error creating contact in the database: {e}")
        raise e


def get_contacts(
    db: Session, user: User, skip: int = 0, limit: int = 10
) -> List[Contact]:
    return (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_contact(db: Session, user: User, contact_id: int) -> Contact:
    return (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )


def update_contact(db: Session, contact_id: int, contact_update: ContactUpdate):
    try:
        logger.info(f"Updating contact in the database: {contact_id}")
        db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if db_contact:
            for key, value in contact_update.model_dump().items():
                setattr(db_contact, key, value)
            db.commit()
            db.refresh(db_contact)
            return db_contact
        return None
    except Exception as e:
        logger.error(f"Error updating contact in the database: {e}")
        raise e


def delete_contact(db: Session, contact_id: int):
    print("I am inside")
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    print(db_contact)
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False

    # try:
    #     # logger.info(f"Deleting contact from the database: {contact_id}")
    #     db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    #     print(db_contact)
    #     if db_contact:
    #         db.delete(db_contact)
    #         db.commit()
    #         return True
    #     return False
    # except Exception as e:
    #     logger.error(f"Error deleting contact from the database: {e}")
    #     raise e


def get_upcoming_birthdays(
    db: Session, start_date: date, end_date: date
) -> List[Contact]:
    try:
        logger.info(
            f"Retrieving upcoming birthdays from the database: {start_date}, {end_date}",
        )
        return (
            db.query(Contact)
            .filter(Contact.birthday.between(start_date, end_date))
            .order_by(Contact.birthday)
            .all()
        )
    except Exception as e:
        logger.error(f"Error retrieving upcoming birthdays from the database: {e}")
        raise e


# def get_user_by_email(db: Session, email: str):
#     return db.query(User).filter(User.email == email).first()
