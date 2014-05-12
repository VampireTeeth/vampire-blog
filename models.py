from mongoengine import Document, StringField, DateTimeField, ReferenceField, ObjectIdField
import bson


class User(Document):
    id = ObjectIdField(primary_key=True, default=lambda:bson.ObjectId())
    email = StringField(max_length=50)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Login(Document):
    username = StringField(max_length=50)
    password = StringField(max_length=32)


class Blog(Document):
    id = ObjectIdField(primary_key=True, default=lambda:bson.ObjectId())
    dateTime = DateTimeField(required=True)
    content = StringField(max_length=1000)
    author = ReferenceField('User')
