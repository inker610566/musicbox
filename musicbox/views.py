from . import app
from flask import render_template, session
from modules.SQL import executeSingleQueryReturn, executeSingleCommand
from modules.SongQuery import getSonglist
import modules.Template.TemplateManager
from modules.Template.Templates import PlayerTemp
from modules.Template.Templates import TagPlayerTemp
from modules.Template.Templates import SongAdminTemp
from modules.Template.Templates import TagAdminTemp
from modules.Template.Templates import TagTemp
import urllib
import os

#def getSongAndUntraceFile():
#	row = executeSingleQueryReturn("SELECT * FROM song")
#	for dirpath, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
#		for f in files:

@app.route("/")
def main():
	tm = TemplateManager()
	# prepare player -- decorator pattern
	player = PlayerTemp()
	player = TagPlayerTemp(player)
	tm.loadComponentTemplate(player)

	if session.get("sid", "") == "A":
		tm.loadHeadTemplate(TagAdminTemp())
		tm.loadComponentTemplate(SongAdminTemp())
	else:
		tm.loadHeadTemplate(TagTemp())
	
	# setup player using decorator pattern
	#params["p_tag_player"] = "component/song_player.refactor.htmld"
	#component_templates.append("component/tag_player.htmld")

	
	#rows = getSonglist()
	#params["untrack_files"] = getUntrackedFile()
	
	#return render_template("test.htmld", header_templates=header_templates, component_templates=component_templates, **params)
	return tm.getRenderHtml()


@app.route("/test")
def test():
	return render_template("lrc.htmld", ptag="player.htmld", plrc="tag.htmld")
