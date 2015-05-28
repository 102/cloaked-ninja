from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app
import sys

port = 80
try:
  port = int(sys.argv[1])
except:
  pass

print 'running on port {0}'.format(port)

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(port)
IOLoop.instance().start()
