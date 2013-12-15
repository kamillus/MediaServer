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

 