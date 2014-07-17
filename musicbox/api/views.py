from .. import app
from flask import render_template, request, session
from Tag.Tag import Tag 
from ..modules.SQL import executeSingleCommand, executeSingleQueryReturn
from ..interfaces.JsonEncodable.JsonEncodable import JsonEncodable
from ..modules.SongQuery import getSonglist
from ..modules.TagQuery import isTagExists, addTagToSong, addTag, getTaglist
import urllib
import os

@app.route("/api/tag/<tagid>", methods=["GET"])
def tag(tagid):
	#if request.method == "GET":
		
	#ctx.close()
	#x = Tag(tagname)
	#return x.encode()

	return "Not Implement Yet";

@app.route("/api/song/<songname>", methods=["GET", "POST"])
def song(songname):
	return "Not Implement Yet";

@app.route("/api/tag", methods=["POST"])
def tagRootPost():
	if session.get("sid", "") != "A":
		return "Failed(session expire)"
	request.form = getattr(request, "form", {})
	if "name" not in request.form or "sid" not in request.form:
		return "Failed(invalid parameter)"
	name = request.form["name"]
	sid = int(request.form["sid"])
	rows = isTagExists(name)
	if not rows:
		if "force" not in request.form:
			return "New"
		else:
			rows = addTag(name)
	tid = rows[0][0]
	addTagToSong(tid, sid)
	return "Done"

@app.route("/api/tag", methods=["GET"])
def tagRootGet():
	if request.args.get("sid", ""):
		result = ""
		rows = getTaglist(request.args.get("sid", ""))
		for row in rows:
			result += JsonEncodable.encodeSQLRow(row, ("id", "name")) + ","
		return "[" + result[:-1] + "]"
	
	return "Failed(Not Implement Yet)"

@app.route("/api/song", methods=["GET"])
def songRootGet():
	params = {}
	if request.args.get("tid", ""):
		params["tagid"] = request.args["tid"]
	result = ""
	rows = getSonglist(**params)
	for row in rows:
		result += JsonEncodable.encodeSQLRow(row, ("id", "name", "location", "image", "lrc")) + ","
	return "[" + result[:-1] + "]"

def checkAllowSongFileType(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_SONG_EXTENSIONS']

def checkAllowImageFileType(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_IMAGE_EXTENSIONS']

def checkAllowFilename(filename):
	return not os.path.split(filename)[0]

@app.route("/api/song", methods=["POST"])
def songRootPost():
	if session.get("sid", "") != "A":
		return "Failed(session expire)"
	# http://flask.pocoo.org/snippets/47/
	# auth check
	#if session.get("sid", "") != "A":
	#	return "Die"
	'''
		loction
		Null: search under UPLOAD_FOLDER
		FILE: upload to UPLOAD_FOLDER
		POST: write to database directly
	'''
	name = location = image = ""
	request.form= getattr(request, "form", {})
	request.files = getattr(request, "files", {})
	
	# check
	if request.files.get("location", False):
		song_file = request.files['location']
		filename = song_file.filename
		if not checkAllowSongFileType(filename):
			return "Failed(song filetype not allowed)"
		if not checkAllowFilename(filename):
			return "Failed(filename not allowed)"
		pathOnServer = os.path.join(app.config['UPLOAD_SONG_FOLDER'], filename)
		if os.path.exists(pathOnServer) and "force" not in request.form:
			return "Failed(file exists)"
		name = getattr(request.form, "name", False) or os.path.splitext(filename)[0]
		# if windows need substitute '\' to '/'
		location = os.path.join(app.config['UPLOAD_SONG_REFER'], urllib.quote(filename.encode("utf-8")))
	elif "location" in request.form:
		location = request.form["location"]
		if "name" not in request.form:
			return "Failed(filename not supplied)"
		name = request.form["name"]
	else:
		return "Failed(location not specified)"

	if request.files.get("image", False):
		image_file = request.files['image']
		filename = image_file.filename
		if not checkAllowImageFileType(filename):
			return "Failed(image filetype not allowed)"
		if not checkAllowFilename(filename):
			return "Failed(filename not allowed)"
		pathOnServer2 = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename)
		if os.path.exists(pathOnServer) and "force" not in request.form:
			return "Failed(file exists)"
		# if windows need substitute '\' to '/'
		image = os.path.join(app.config['UPLOAD_IMAGE_REFER'], urllib.quote(filename.encode("utf-8")))
	
	# commit change
	if request.files.get("location", False):
		song_file.save(pathOnServer)
	if request.files.get("image", False):
		image_file.save(pathOnServer2)

	if "force" not in request.form:# avoid duplicate entry in database
		executeSingleCommand("INSERT INTO song (name, location, image) VALUES(%s, %s, %s)", (name, location, image or None))
	return "Done"
	


if __name__ == "__main__":
	app.run(debug=True)
