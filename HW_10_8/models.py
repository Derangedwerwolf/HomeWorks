from mongoengine import *
import connector


class Authors(Document):
    fullname = StringField(max_length=100)
    born_date = StringField(max_length=20)
    born_location = StringField(max_length=100)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=30))
    author_ref = ReferenceField(Authors, reverse_delete_rule=CASCADE, dbref = False)
    author = StringField(max_length=100)
    quote = StringField()
    #meta = {'allow_inheritance': True}

    