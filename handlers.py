import tornado.web
from models import User


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
                    title='Index',
                    message='Hello, world!',
                    users=User.objects())

class UserHandler(tornado.web.RequestHandler):
    def post(self):
        # print self.request.arguments
        firstname = self.request.arguments['firstname'][0]
        lastname = self.request.arguments['lastname'][0]
        email= self.request.arguments['email'][0]
        _add_user(email, firstname, lastname)
        self.redirect('/')

def _add_user(email, first_name, last_name):
    User(email=email, first_name=first_name, last_name=last_name).save()


