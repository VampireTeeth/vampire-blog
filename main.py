import os.path

import tornado.ioloop
import tornado.web
from mongoengine import Document, StringField, connect


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    # meta = {'db_alias': 'vampireteeth-blog'}

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


if __name__ == '__main__':

    connect('vampire-blog')
    settings = {
        'template_path': os.path.join(
            os.path.dirname(__file__), 'templates'),
    }

    app = tornado.web.Application([
        (r'/', MainHandler),
        (r'/user', UserHandler),
    ], **settings)

    app.listen(8888)
    print "Listening on 8888...."
    tornado.ioloop.IOLoop.instance().start()

