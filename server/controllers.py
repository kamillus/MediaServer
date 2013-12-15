import cherrypy
import json
import os
from client.settings import Settings
from PyQt4.QtCore import *
from jinja2 import Environment, FileSystemLoader
import subprocess

class Server(QThread):
    static_directory = ""
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while(1):
            cherrypy.quickstart(Root(), "/", {
                "global": {"server.socket_port": 1345, "server.socket_host": "0.0.0.0"},
                "/static": {"tools.staticdir.dir": os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "static")), "tools.staticdir.on": "True"},
                #"/static_media": {"tools.staticdir.dir": self.static_directory, "tools.staticdir.on": "True"},    
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

    @cherrypy.expose  
    def get_file(self, file_hash):
        settings = Settings() 
        libraries = settings.library
        result = {}

        for library in libraries.iteritems():
            print library
            for item in library[1]["library"]:
                if item["hash"] == file_hash:
                    result = item

        cherrypy.response.headers['Content-Type'] = ContentTypeSelector().get_content_type(result["filename"])
        media_file = open(result["path"], 'rb') 
        return self.file_generator(media_file)
        #return json.dumps(result)

    def file_generator(self, f):
        for data in f:
            yield data

    @cherrypy.expose
    def start_stream(self, path):
        try:
            self.stream.stop()
        except:
            print "Stream not running."

        self.stream = VideoStream()
        print "path"
        print path
        self.stream.set_stream_path(path)
        self.stream.set_stream_to_ip(cherrypy.request.remote.ip)
        self.stream.start()

class VideoStream(QThread):
    vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"

    def __init__(self):
        QThread.__init__(self)
    
    def set_stream_to_ip(self, ip):
        self.remote_ip = ip

    def set_stream_path(self, path):
        self.stream_path = path

    def get_vlc_command(self):
        return [self.vlc_path, self.stream_path, "-I", "dummy", "--vout=dummy", "#duplicate{dst=display,dst=\"transcode{vcodec=mp4v,acodec=mpga,vb=800,ab=128,deinterlace}:rtp{mux=ts,dst=" + self.remote_ip + ",sdp=sap,name=\"VideoStream\"}\"}"]

    def run(self):
        print self.get_vlc_command()
        print " ".join(self.get_vlc_command())
        process = subprocess.Popen(" ".join(self.get_vlc_command()), shell=True, stdout=subprocess.PIPE)
        process.wait()

class ContentTypeSelector(object):

    def get_content_type(self, file):
        filename, file_extension = os.path.splitext(file)

        if ".mkv" in file_extension: return "video/x-matroska"
        if ".avi" in file_extension: return "video/x-msvideo"
        if ".mp4" in file_extension: return "video/mp4"
        if ".mp3" in file_extension: return "audio/mpeg"
        if ".m4a" in file_extension: return "audio/m4a"
