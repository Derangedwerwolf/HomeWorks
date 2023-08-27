import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List

from services.auth_manager import auth_manager
from api.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from database.models import User
from database.db import get_db
from database.crud import (
    create_contact,
    get_contact,
    get_contacts,
    update_contact,
    delete_contact as delete,
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse)
def create_new_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_manager.get_current_user),
):
    try:
        logger.info(f"Creating a new contact: {contact}")
        return create_contact(db=db, user_id=current_user.id, contact=contact)
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=List[ContactResponse])
def read_contacts(
    skip: int = Query(default=0),
    limit: int = Query(default=10),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_manager.get_current_user),
):
    try:
        logger.info(f"Retrieving contacts with pagination: {skip}, {limit}")
        return get_contacts(db=db, user_id=current_user.id, skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Error retrieving contacts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{contact_id}/", response_model=ContactResponse)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_manager.get_current_user),
):
    try:
        logger.info(f"Retrieving contact by ID: {contact_id}")
        contact = get_contact(db=db, user=current_user, contact_id=contact_id)

        if not contact:
            logger.warning(f"Contact not found: {contact_id}")
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except Exception as e:
        logger.error(f"Error retrieving contact: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{contact_id}/", response_model=ContactResponse)
def update_contact_details(
    contact_id: int,
    contact_update: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_manager.get_current_user),
):
    contact = get_contact(db=db, user=current_user, contact_id=contact_id)

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    try:
        logger.info(f"Updating contact details: {contact_id}")
        updated_contact = update_contact(
            db=db, contact_id=contact_id, contact_update=contact_update
        )
        if updated_contact is None:
            logger.warning(f"Failed to update contact: {contact_id}")
            raise HTTPException(status_code=500, detail="Failed to update contact")
        return updated_contact
    except Exception as e:
        logger.error(f"Error updating contact: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{contact_id}/")
def delete_contact(
    contact_id: int = Path(ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_manager.get_current_user),
):
    contact = get_contact(db=db, user=current_user, contact_id=contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    try:
        logger.info(f"Deleting contact: {contact_id}")
        if not delete(db=db, contact_id=contact_id):
            logger.warning(f"Failed to delete contact: {contact_id}")
            raise HTTPException(status_code=500, detail="Failed to delete contact")
        return None  # Return None for a successful delete operation
    except Exception as e:
        logger.error(f"Error deleting contact: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
