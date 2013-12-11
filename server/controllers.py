import cherrypy
import json
import os
from client.settings import Settings
from PyQt4.QtCore import *
from jinja2 import Environment, FileSystemLoader

class Server(QThread):
    static_directory = ""
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while(1):
            cherrypy.quickstart(Root(), "/", {
                "global": {"server.socket_port": 1345},
                "/static": {"tools.staticdir.dir": os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "static")), "tools.staticdir.on": "True"},
                "/static_media": {"tools.staticdir.dir": self.static_directory, "tools.staticdir.on": "True"},    
            })  
        
class Root(object):
    env = Environment(loader=FileSystemLoader('templates'))
    streaming_thread = None

    @cherrypy.expose
    def index(self):
        settings = Settings() 
        tmpl = self.env.get_template('index.html')
        return tmpl.render(libraries=None)
    
    @cherrypy.expose        
    def get_library(self):
        settings = Settings() 
        return json.dumps(settings.library)

class VideoStream(QThread):
    def __init__(self, path=None):
        self.stream_path = "/Users/kawid/Graboid/Completed/6034630_-_Parks_and_Recreation_-_4x13/parks.and.recreation.413.hdtv-lol.avi"
        QThread.__init__(self)
        
    def run(self):
        while(1):
            print "hello"
            self.process_path()
            self.finish()
            time.sleep(200)