import mongoengine as mg
import bson
from datetime import datetime


class User(mg.Document):
    email = mg.StringField(max_length=50, required=True, primary_key=True)
    password = mg.StringField(max_length=32)
    first_name = mg.StringField(max_length=50)
    last_name = mg.StringField(max_length=50)


class Login(mg.Document):
    username = mg.StringField(max_length=50)
    password = mg.StringField(max_length=32)



class Article(mg.Document):
    id = mg.ObjectIdField(primary_key=True, default=lambda:bson.ObjectId())
    dateTime = mg.DateTimeField(required=True, default=lambda:datetime.now())
    title = mg.StringField(required=True)
    content = mg.StringField(max_length=1000)
    voted = mg.IntField(default=0)
    author = mg.ReferenceField('User', required=True)


class Comment(mg.Document):
    id = mg.ObjectIdField(primary_key=True, default=lambda:bson.ObjectId())
    dateTime = mg.DateTimeField(required=True, default=lambda:datetime.now())
    content = mg.StringField(max_length=1000)

class Vote(mg.Document):
    id = mg.ObjectIdField(primary_key=True, default=lambda:bson.ObjectIdField())
    article = mg.ReferenceField('Article', required=True)
    user = mg.ReferenceField('User', required=True)
    pass

