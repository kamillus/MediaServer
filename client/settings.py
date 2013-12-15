import os
import json
import socket

class Settings(object):
    protocol = "http"
    host = socket.gethostbyname(socket.gethostname())
    port = "1345"
    user_settings_directory = "~/.MediaServer"
    settings_file = "settings"
    library_file = "library"
    file_paths = []
    library = {}
    settings = {}
    icon_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "..", "icon.png"))
    
    def __init__(self):  
        if not os.path.exists(self.icon_path):
            self.icon_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../..", "icon.png"))    

        self.create_user_dirs()
        self.get_media_library()
        self.get_config_from_files()
    
    def get_server_address(self):
        return self.protocol + "://" + self.host + ":" + self.port
        
    def create_user_dirs(self):
        if not os.path.exists(self.get_settings_directory()):
            os.makedirs(self.get_settings_directory())
    
    def get_settings_directory(self):
        return os.path.abspath(os.path.expanduser(self.user_settings_directory))
            
    def get_settings_file_path(self):
        return os.path.abspath(os.path.expanduser(os.path.join(self.user_settings_directory, self.settings_file)))
        
    def get_library_file_path(self):
        return os.path.abspath(os.path.expanduser(os.path.join(self.user_settings_directory, self.library_file)))
    
    def get_config_from_files(self):
        try:
            f = open(self.get_settings_file_path(), 'r')
            self.settings = json.loads(f.read())
            f.close()
        except Exception as e:
            print e
            self.settings = {"file_paths": [os.path.expanduser("~")]}
            f = open(self.get_settings_file_path(), 'w')
            f.write(json.dumps(self.settings))
            f.close()
            
        self.file_paths = self.settings["file_paths"]

    def get_media_library(self):
        try:
            f = open(self.get_library_file_path(), 'r')
            self.library = json.loads(f.read())
            f.close()
        
        except Exception as e:
            print e
            self.library = {}

            f = open(self.get_library_file_path(), 'w')
            f.write(json.dumps(self.library))
            f.close()        

    def write_library(self, library, index):
        print "Writing to: " + self.get_library_file_path()
        print index
        self.library[index] = {"library": library}
        f = open(self.get_library_file_path(), 'w')
        f.write(json.dumps(self.library))
        f.close()        
        
        