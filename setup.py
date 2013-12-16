from setuptools import setup
import sys
import os

if sys.platform == "darwin":
    plist = {
                "LSUIElement" : True,
                'CFBundleIdentifier': 'ca.kamil.ams',
                'NSPrincipalClass': 'NSApplication',
                'NSHighResolutionCapable': 'True'
            }

    data = [
            ('static/css/', ['static/css/app.css']),
            ('static/js/', ['static/js/controllers.js']),
            ('static/js/', ['static/js/app.js']),
            ('static/js/extras', ['static/js/extras/angular-route.js']),
            ('static/partials/', ['static/partials/video-detail.html']),
            ('static/partials/', ['static/partials/video-list.html']),
            ('static/partials/', ['static/partials/music_player.html']),
            ('templates/', ['templates/index.html']),
            ('templates/', ['templates/base.html']),
            ('lib/python2.7/', ['icon.png']),
            ]


    app = ['MediaServer.py']
    options = {'argv_emulation': True,
    'plist': plist,
    'iconfile':'icon.icns',
    }

    setup(
        app=app,
        name='Awesome Media Server',
        options={'py2app': options},
        data_files=data,
        setup_requires=['py2app'],
    )

if sys.platform == "win32":
    import py2exe
    data = [
            ('static\\css\\', ['static\\css\\app.css']),
            ('static\\js\\', ['static\\js\\controllers.js']),
            ('static\\js\\', ['static\\js\\app.js']),
            ('static\\js\\extras', ['static\\js\\extras\\angular-route.js']),
            ('static\\partials\\', ['static\\partials\\video-detail.html']),
            ('static\\partials\\', ['static\\partials\\video-list.html']),
            ('static\\partials\\', ['static\\partials\\music_player.html']),
            ('templates\\', ['templates\\index.html']),
            ('templates\\', ['templates\\base.html']),
            ('lib\\python2.7\\', ['icon.png']),
            ]


    app = ['MediaServer.py']
    options = {
        'excludes':['PyQt4.QtDesigner','PyQt4.QtOpenGl','PyQt4.QtScript','PyQt4.QtSql','PyQt4.QtTest','PyQt4.QtXml','PyQt4.phonon', 'PyQt4.QtHelp', 'PyQt4.QtDeclarative', 'PyQt4.QtDeclarative'],
        "bundle_files": 3,
        'includes': ["sip", "client", "server"]
    }

    program = [
        {
            "script": "MediaServer.py",
            "icon_resources": [(1, "icon.ico")],
            "dest_base": "Awesome Media Server",
            "description": "Play media from your computer in the browser",
            "author": "Awid.ca",
        },
    ]

    setup(
        data_files=data,
        options={'py2exe': options},
        windows=program,
        name="Graboid",

    )