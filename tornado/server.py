#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("default.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    
    def check_origin(self, origin):
        return True
    
    def open(self):
        self.set_nodelay(True)
        print('Socket Connected: ' + str(self.request.remote_ip))
        self.write_message("connected")
        WebSocketHandler.waiters.add(self)
    
    def on_message(self, message):
        self.write_message(u"message recieved: " + message)
        print "message received " + message
    
    def on_close(self):
        WebSocketHandler.waiters.remove(self)
    
    @classmethod
    def send_updates(cls, index):
        for waiter in cls.waiters:
            try:
                waiter.write_message(index)
            except:
                print("Error sending message")


application = tornado.web.Application([
                                       (r"/", MainHandler),
                                       (r"/websocket", WebSocketHandler),
                                       ])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8889)
    tornado.ioloop.IOLoop.instance().start()