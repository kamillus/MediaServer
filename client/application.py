from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from server.controllers import *
from settings import *
from media import *
import sys

class Application(object):
    def main(self):
        self.app = QtGui.QApplication(sys.argv)
        
        self.settings = Settings()
        self.media_collectors = []
        self.media_collectors.append(MediaCollector(path=self.settings.file_paths[0]))
        self.media_collectors[0].finish_func = self.settings.write_library
        self.media_collectors[0].start()
        
        self.main_widget = ApplicationWidget()
        self.main_widget.hide()
        self.main_widget.set_application_exit(self.app.exit)
        self.main_widget.set_app_url_settings(self.settings.get_server_address())
        
        icon = QApplication.style().standardIcon(QStyle.SP_DriveNetIcon)     
        self.tray_widget = MediaTray(parent=self.main_widget, icon=icon)
        
        self.server = Server()
        self.server.start()
        
        self.tray_widget.show()
        sys.exit(self.app.exec_())
        
class ApplicationWidget(QtGui.QWidget):
    def open(self):
        print self.app_url
        QDesktopServices.openUrl(QUrl(self.app_url))
        
    def exit(self):
        print "exit"
        try:
            self.exit_command()    
        except Exception as e:
            print e
        
    def set_application_exit(self, exit_command):
        self.exit_command = exit_command
        
    def set_app_url_settings(self, url):
        self.app_url = url


class MediaTray(QtGui.QSystemTrayIcon):
    def __init__(self, icon=None, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.parent = parent
        menu = QtGui.QMenu(self.parent)        
        
        self.setActions()
        openAction = menu.addAction(self.openAction)
        exitAction = menu.addAction(self.exitAction)
        self.setContextMenu(menu)
        
    def setActions(self):
        self.openAction = QtGui.QAction(self.tr("Open"), self)
        QObject.connect(self.openAction, SIGNAL("triggered()"), self.parent.open)
        
        self.exitAction = QtGui.QAction(self.tr("Exit"), self)
        QObject.connect(self.exitAction, SIGNAL("triggered()"), self.parent.exit)
    
    