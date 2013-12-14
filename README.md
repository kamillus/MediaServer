Awesome Media Server
===========

Lightweight media scanning and file access server. 

#Purpose

Awesome Media Server indexes video and music files on your hard drive for remote access through a simple search engine. Access all your favourite videos and music from anywhere including your tablets and phones. 

#What is needed to run AMS?
In the future binary downloads will be provided for different operating systems (Mac, PC, Linux). But for now, the only way to run is by installing the packages below before running the app:

* cherrypy
* QT4

#How to run

```python
	python MediaServer.py
```

#Problems
* As of this moment, the only way to play the media on an ipad or tablets is by copying and pasting the url provided into VLC (which is freely downloadable) in the Open Network Stream tab.
* The only way to change the scanning path is by modifying the config file in ~/.MediaServer. The file will be generated on first run. 