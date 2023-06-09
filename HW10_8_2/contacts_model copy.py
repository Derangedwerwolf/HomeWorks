from mongoengine import *
import connector

   
class Contact(Document):
    full_name = StringField(required=True)
    user_age = IntField(max_length=3)
    user_profession = StringField()
    phone_number = StringField(required=True)
    preferred_delivery_method = StringField(choices=["SMS", "Email"], required=True, default="Email")
    email = EmailField(required=True)
    is_sent = BooleanField(default=False)