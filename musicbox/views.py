from . import app
from flask import render_template, session
from modules.SQL import executeSingleQueryReturn, executeSingleCommand
from modules.SongQuery import getSonglist
import urllib
import os

#def getSongAndUntraceFile():
#	row = executeSingleQueryReturn("SELECT * FROM song")
#	for dirpath, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
#		for f in files:

@app.route("/")
def main():
	header_templates = []
	component_templates = []
	params = dict()
	if session.get("sid", "") == "A":
		header_templates.append("header/tag_admin.htmld")
		component_templates.append("component/song_admin.htmld")
	else:
		header_templates.append("header/tag.htmld")
	
	# setup player using decorator pattern
	params["p_tag_player"] = "component/song_player.refactor.htmld"
	component_templates.append("component/tag_player.htmld")

	
	#rows = getSonglist()
	#params["untrack_files"] = getUntrackedFile()
	
	return render_template("test.htmld", header_templates=header_templates, component_templates=component_templates, **params)


@app.route("/test")
def test():
	return render_template("lrc.htmld", ptag="player.htmld", plrc="tag.htmld")
