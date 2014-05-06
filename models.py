

from mongoengine import Document, StringField


class User(Document):
    email = StringField(max_length=50)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
