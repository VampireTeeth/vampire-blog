from mongoengine import Document, StringField


class User(Document):
    email = StringField(max_length=50)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Login(Document):
    username = StringField(max_length=50)
    password = StringField(max_length=32)
