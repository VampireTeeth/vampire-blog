import tornado.web
from models import User




class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        self.kwargs = kwargs
        print 'keyword args:', self.kwargs

    def prepare(self):
        print 'arguments:'
        print self.request.arguments
        print 'query arguments arg1:'
        print self.get_query_arguments('arg1')
        print 'body arguments firstname:'
        print self.get_body_arguments('firstname')


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('index.html',
                    title='Index',
                    message='Hello, world!',
                    users=User.objects())

class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        # print self.request.arguments
        firstname = self.request.arguments['firstname'][0]
        lastname = self.request.arguments['lastname'][0]
        email= self.request.arguments['email'][0]
        _add_user(email, firstname, lastname)
        self.redirect('/')

def _add_user(email, first_name, last_name):
    User(email=email, first_name=first_name, last_name=last_name).save()

class LoginHandler(BaseHandler):
    def get(self):
        print 'login get'
    def post(self):
        #TODO
        pass

