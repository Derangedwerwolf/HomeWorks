import logging
from sqlalchemy.orm import Session
from .models import Contact
from api.schemas.contact import ContactCreate, ContactUpdate

from datetime import date
from typing import List

logger = logging.getLogger(__name__)


def create_contact(db: Session, contact: ContactCreate):
    try:
        logger.info(f"Creating a new contact in the database: {contact}")
        # contact_dict = contact.dict()  # Convert ContactCreate to a dictionary
        db_contact = Contact(**contact.dict())
        # db_contact = Contact(**contact.model_dump())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except Exception as e:
        logger.error(f"Error creating contact in the database: {e}")
        raise e


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 10) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


def update_contact(db: Session, contact_id: int, contact_update: ContactUpdate):
    try:
        logger.info(f"Updating contact in the database: {contact_id}")
        db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if db_contact:
            for key, value in contact_update.dict().items():
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
            .filter(Contact.birthday >= start_date, Contact.birthday <= end_date)
            .order_by(Contact.birthday)
            .all()
        )
    except Exception as e:
        logger.error(f"Error retrieving upcoming birthdays from the database: {e}")
        raise e
