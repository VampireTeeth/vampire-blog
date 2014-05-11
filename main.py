import os.path

import tornado.ioloop
import tornado.web
from mongoengine import connect
from handlers import MainHandler, UserHandler, LoginHandler, SignupHandler, LogoutHandler



if __name__ == '__main__':

    db = 'vampire-blog'
    connect(db)
    
    settings = {
        'template_path': os.path.join(
            os.path.dirname(__file__), 'templates'),
        'login_url': r'/login',
        'cookie_secret': '26aac492159b5f66f196cbe496327ee937731357',
        'debug': True,
    }

    app = tornado.web.Application([
        (r'/user', UserHandler),
        (r'/login', LoginHandler),
        (r'/signup', SignupHandler),
        (r'/logout', LogoutHandler),
        (r'/.*', MainHandler, dict(db=db)),
    ], **settings)

    app.listen(8888)
    print "Listening on 8888...."
    tornado.ioloop.IOLoop.instance().start()

