from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime, date


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_data: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True


class ContactBirthdayResponse(ContactBase):
    days_until_birthday: int
