import tornado.web
import tornado.ioloop
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
import server_config
import random
import time


chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
ccount = len(chars)-1
def get_unique_id():
    s = ''
    for i in xrange(0,9):
        s += chars[random.randint(0,ccount)]
    return s

# Base class that sets up SQLAlchemy DB session
class BaseDBHandler(tornado.web.RequestHandler):
  def initialize(self, session):
    self.session = session

  def prepare(self):
    self.db = self.session()

  def on_finish(self):
    self.db.close()

  def get_current_user(self):
    sid = self.get_secure_cookie('session_id')
    return sid

class AuthLoginHandler(BaseDBHandler):
  def get(self):
    sid = self.get_secure_cookie('session_id')
    redir = self.get_argument('next', default='/')
    if sid:
      print "login: got sid: ", sid
      print "login get redir: ", redir
      self.redirect(redir)
    else:
      # not logged in, show login page
      self.render('login.html', next=redir)

  def post(self):
    # TODO: check first
    sid = get_unique_id()
    self.set_secure_cookie('session_id', sid)
    redir = self.get_argument('next', default='/')
    print "login post redir: ", redir
    self.redirect(redir)

class AuthLogoutHandler(BaseDBHandler):
  def get(self):
    self.clear_cookie('session_id')
    redir = self.get_query_argument('next', default='/')
    print "logout redir: ", redir
    self.redirect(redir)

class ListHandler(BaseDBHandler):
  @tornado.web.authenticated
  def get(self):
    print "list get"
    self.render('list.html')

class MainHandler(BaseDBHandler):
  def get(self):
    sid = self.get_secure_cookie('session_id')
    print "main: sid: ", sid
    #self.db.query()
    self.render('main.html')

db_settings = {
  'host': server_config.dbhost
}
if server_config.dbdriver != 'sqlite':
  db_settings['username'] = server_config.dbuser
  db_settings['password'] = server_config.dbpass
else:
  db_settings['host'] = '/'+server_config.dbhost

#engine = create_engine(URL(server_config.dbdriver, **db_settings))
engine = create_engine(server_config.dbdriver+':///'+server_config.dbhost)
Session = sessionmaker(bind=engine)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      tornado.web.URLSpec(r'/', MainHandler, {'session': Session}, 'root'),
      tornado.web.URLSpec(r'/list/*', ListHandler, {'session': Session}, 'list'),
      tornado.web.URLSpec(r'/auth/login/*', AuthLoginHandler, {'session': Session}, 'login'),
      tornado.web.URLSpec(r'/auth/logout/*', AuthLogoutHandler, {'session': Session}, 'logout'),
    ]
    settings = {
      'cookie_secret': server_config.cookie_secret,
      'login_url': '/auth/login/'
    }
    tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
  application = Application()
  application.listen(8000)
  tornado.ioloop.IOLoop.instance().start()

