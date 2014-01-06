import cherrypy
import json
import os
from client.settings import Settings
from PyQt4.QtCore import *
from jinja2 import Environment, FileSystemLoader
import subprocess
from mutagen.mp3 import MP3
from mutagen import File

class Server(QThread):
    static_directory = ""
    port = ""
    host = ""
    
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        static_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "static"))
        if not os.path.exists(static_path):
            static_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../../../../", "static"))
        if not os.path.exists(static_path):
            static_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../../", "static"))

        while(1):
            cherrypy.quickstart(Root(), "/", {
                "global": {"server.socket_port": self.port, "server.socket_host": self.host},
                "/static": {"tools.staticdir.dir": static_path, "tools.staticdir.on": "True"},
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

    def find_item(self, file_hash):
        settings = Settings() 
        libraries = settings.library
        result = {}

        for library in libraries.iteritems():
            for item in library[1]["library"]:
                if item["hash"] == file_hash:
                    result = item

        return result


    @cherrypy.expose
    def get_file_tags(self, file_hash):
        item = self.find_item(file_hash)
        info = MP3(item["path"])

        return json.dumps(info.pprint())



    @cherrypy.expose
    def get_cover_art(self, file_hash):
        item = self.find_item(file_hash)
        filename, file_extension = os.path.splitext(item["filename"])

        try:
            file = File(item["path"])
            artwork = None
            if file_extension == ".m4a":
                artwork = file.tags["data"]["tag"][0]
            if file_extension == ".mp3":
                artwork = file.tags['APIC:'].data

            cherrypy.response.headers['Content-Type'] = file.tags['APIC:'].mime
        except:
            artwork = None
            
        return artwork

    @cherrypy.expose  
    def stream_file(self, file_hash):
        settings = Settings() 
        libraries = settings.library
        result = {}

        for library in libraries.iteritems():
            for item in library[1]["library"]:
                if item["hash"] == file_hash:
                    result = item

        cherrypy.response.headers['Content-Type'] = ContentTypeSelector().get_content_type(result["filename"])
        cherrypy.response.headers["Content-Length"] = os.path.getsize(result["path"])
        #cherrypy.response.headers["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(result["filename"])
        media_file = open(result["path"], 'rb') 
        return self.file_generator(media_file)
        #return json.dumps(result)

    def file_generator(self, f):
        data = f.read(1024*8)
        try:
            while len(data) > 0:
                yield data
                data = f.read(1024*8)
                
        except:
            f.close()
        f.close()
    stream_file._cp_config = {'response.stream': True}

    @cherrypy.expose
    def get_file(self, file_hash):
        settings = Settings() 
        libraries = settings.library
        result = {}

        for library in libraries.iteritems():
            for item in library[1]["library"]:
                if item["hash"] == file_hash:
                    result = item

        return json.dumps(result)        

    @cherrypy.expose
    def start_stream(self, path):
        try:
            self.stream.stop()
        except:
            print "Stream not running."

        self.stream = VideoStream()
        print "path"
        #print path
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
