import tornado.web
import tornado.escape
from models import User, Article



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

    def set_current_user(self, user):
        if user:
            d = {'email' : user.email, 'firstname':user.first_name, 'lastname':user.last_name}
            self.set_secure_cookie('user', tornado.escape.json_encode(d))
        else:
            self.clear_cookie('user')


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        d = tornado.escape.json_decode(self.current_user)
        users = User.objects(email=d['email'])
        if users:
          u = users[0]
          self.render('index.html',
                    title='Index',
                    message='Hello, %s %s' % (d['firstname'], d['lastname']),
                    errormsg=self.get_argument('errormsg', ''),
                    articles=Article.objects(author=u))

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
                message='Please input your information below to signup', 
                errormsg=self.get_argument('errormsg', ''))

    def post(self):
        email = self.get_argument('email')
        users = User.objects(email=email)
        if users:
            error = '?errormsg=' + tornado.escape.url_escape('User already exists')
            self.redirect(u'/signup' + error)
        else:
            firstname = self.get_argument('firstname')
            lastname = self.get_argument('lastname')
            password = self.get_argument('password')
            u = User(email=email, first_name=firstname, last_name=lastname, password=password).save()
            self.set_current_user(u)
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
        email = self.get_argument('email')
        password = self.get_argument('password')
        print email, password
        u, err = self.check_permission(email, password)
        if u:
            print 'Authenticated'
            self.set_current_user(u)
            self.redirect(self.get_argument('next', u'/'))
        else:
            error = '?errormsg=' + tornado.escape.url_escape(err)
            self.redirect(u'/login' + error)

    def check_permission(self, email, password):
        users = User.objects(email=email)
        if users:
            if password == users[0].password:
                return users[0], None
            else:
                return None, 'Incorrect password'
        else:
            return None, 'User inexists'

    
class LogoutHandler(BaseHandler):
    def get(self):
        self.set_current_user(None)
        self.redirect('/')


class ArticleHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):
        u = tornado.escape.json_decode(self.current_user)
        title = self.get_argument('title')
        content = self.get_argument('content')
        if not title: 
            self.redirect(r'/?errormsg=' + tornado.escape.url_escape('Title cannot be empty'))
        elif not content:
            self.redirect(r'/?errormsg=' + tornado.escape.url_escape('Content cannot be empty'))
        else:
            users = User.objects(email=u['email'])
            if users:
                u = users[0]
                Article(title=title, content=content, author=u).save()
                self.redirect(r'/')

