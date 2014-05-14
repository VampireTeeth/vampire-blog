import tornado.web
import tornado.escape
from models import User, Login




class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, **kwargs):
        self.kwargs = kwargs
        print '-' * 30
        print 'keyword args:', self.kwargs

    def prepare(self):
        print 'arguments:'
        print self.request.arguments

    def get_current_user(self):
        return self.get_secure_cookie('user')

    def set_current_user(self, username):
        if username:
            self.set_secure_cookie('user', tornado.escape.json_encode(username))
        else:
            self.clear_cookie('user')


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('index.html',
                    title='Index',
                    message='Hello, %s' % (tornado.escape.json_decode(self.current_user),),
                    users=User.objects())

class UserHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        # print self.request.arguments
        firstname = self.request.arguments['firstname'][0]
        lastname = self.request.arguments['lastname'][0]
        email= self.request.arguments['email'][0]
        self._add_user(email, firstname, lastname)
        self.redirect('/')

    def _add_user(self, email, first_name, last_name):
        User(email=email, first_name=first_name, last_name=last_name).save()


class SignupHandler(BaseHandler):

    def get(self):
        self.render('signup.html',
                title='Signup',
                message='Please input your information below to signup')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        Login(username=username, password=password).save()
        self.set_current_user(username)
        self.redirect('/')


class LoginHandler(BaseHandler):

    def get(self):
        if self.get_current_user():
            self.redirect('/')
        else:
            self.render('login.html', 
                    title='Login', 
                    message="Please login first",
                    errormsg=self.get_argument('errormsg', ''))

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        print username, password
        if self.check_permission(username, password):
            print 'Authenticated'
            self.set_current_user(username)
            self.redirect(self.get_argument('next', u'/'))
        else:
            error = '?errormsg=' + tornado.escape.url_escape('Login incorrect')
            self.redirect(u'/login' + error)

    def check_permission(self, username, password):
        users = Login.objects(username=username)
        if users:
            return password == users[0].password
        else:
            return False;

    
class LogoutHandler(BaseHandler):
    def get(self):
        self.set_current_user(None)
        self.redirect('/')
