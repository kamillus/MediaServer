import cherrypy
import json
import os
from client.settings import Settings
from PyQt4.QtCore import *
from jinja2 import Environment, FileSystemLoader

class Server(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while(1):
            cherrypy.quickstart(Root(), "/", {
                "global": {"tools.staticdir.root": os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..")), "server.socket_port": 1345},
                "/static": {"tools.staticdir.dir": "static", "tools.staticdir.on": "True"},
                
            })  
        
class Root(object):
    env = Environment(loader=FileSystemLoader('templates'))

    @cherrypy.expose
    def index(self):
        settings = Settings() 
        tmpl = self.env.get_template('index.html')
        return tmpl.render(libraries=None)
    
    @cherrypy.expose        
    def get_library(self):
        settings = Settings() 
        return json.dumps(settings.library)