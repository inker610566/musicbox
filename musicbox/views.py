from . import app
from flask import session
from modules.SQL import executeSingleQueryReturn, executeSingleCommand
from modules.SongQuery import getSonglist
from modules.Template.TemplateManager import TemplateManager
from modules.Template.Templates.PlayerTemp import PlayerTemp
from modules.Template.Templates.TagPlayerTemp import TagPlayerTemp
from modules.Template.Templates.LrcPlayerTemp import LrcPlayerTemp
from modules.Template.Templates.SongAdminTemp import SongAdminTemp
from modules.Template.Templates.TagAdminTemp import TagAdminTemp
from modules.Template.Templates.TagTemp import TagTemp
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
	player = LrcPlayerTemp(player)
	tm.loadComponentTemplate(player)

	if session.get("sid", "") == "A":
		tm.loadHeadTemplate(TagAdminTemp())
		tm.loadComponentTemplate(SongAdminTemp())
	else:
		tm.loadHeadTemplate(TagTemp())
	
	return tm.getHtml()


@app.route("/test")
def test():
	return render_template("lrc.htmld", ptag="player.htmld", plrc="tag.htmld")
