from mongoengine import *
import connector


class Contact(Document):
    full_name = StringField(required=True)
    user_age = IntField(max_length=3)
    user_profession = StringField()
    email = EmailField(required=True)
    is_sent = BooleanField(default=False)