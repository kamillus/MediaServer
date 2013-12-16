import time
import os
from PyQt4.QtCore import *
import hashlib
import time


class MediaCollector(QThread):
    index_path = ""
    finish_func = None
    media_library = []
    
    def __init__(self, path=None):
        self.index_path = path
        QThread.__init__(self)
        
    def run(self):
        while(1):
            print "hello"
            self.process_path()
            self.finish()
            time.sleep(36000)
            
    def process_path(self):
        extension_processor = FileExtensionProcessor()
        media_library = []
        for dirpath, dirnames, filenames in os.walk(self.index_path):
            for filename in filenames:
                try:
                    name, extension = os.path.splitext(filename)
                    if extension_processor.check_extension(extension):
                        print os.path.join(dirpath, filename)
                        media_library.append(
                            {
                                "filename": filename,
                                "directory": dirpath,
                                "path": os.path.join(dirpath, filename),
                                "hash": hashlib.md5(os.path.join(dirpath, filename).encode('utf8')).hexdigest(),
                                "timestamp": os.path.getctime(os.path.join(dirpath, filename))                     
                            }
                        )
                        
                except Exception as e:
                    print e
            self.media_library = media_library
    
    def finish(self):
        try:
            self.finish_func(self.media_library, self.index_path)
        except Exception as e:
            print e
                
class FileExtensionProcessor():
    extensions = [".mkv", ".avi", ".mp4", ".mp3", ".m4a"]

    def check_extension(self, extension):
        #print extension
        #print self.extensions
        if extension in self.extensions:
            return True
        else:
            return False
    
    def set_extensions(self, extensions):
        self.extensions = extensions