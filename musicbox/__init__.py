from flask import Flask
from flask import render_template
import os

app = Flask(__name__)
app.debug = True

# absolute path for copy file
app.config['UPLOAD_SONG_FOLDER'] = "/home/mbox/public_html/music/"
# web path for apache refered
app.config['UPLOAD_SONG_REFER'] = "/~mbox/music/"
# absolute path for copy file
app.config['UPLOAD_IMAGE_FOLDER'] = "/home/mbox/public_html/image/"
# web path for apache refered
app.config['UPLOAD_IMAGE_REFER'] = "/~mbox/image/"
app.config['ALLOWED_SONG_EXTENSIONS'] = {"mp3", "mp4", "ogg"} 
app.config['ALLOWED_IMAGE_EXTENSIONS'] = {"jpg", "jpeg", "png", "bmp"}
# path for api
app.config['API_REFER'] = "/musicbox/api/"
# for https
app.secret_key = os.urandom(24)
import api.views
import views
import admin.views
