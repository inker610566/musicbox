# A database interface
from ..SQL import executeSingleQueryReturn, executeSingleCommand

def getTaglist(songid=0, limit=-1, offset=-1):
	if songid:
		#tfield = " tag.id, tag.name "
		tfield = " tag.* "
		join_str = " FROM taglist INNER JOIN tag ON taglist.tid=tag.id WHERE sid=%s "
		if limit != -1:
			if offset != -1:
				rows = executeSingleQueryReturn("SELECT"+tfield+join_str+"LIMIT %s,%s", (songid, offset, limit))
			else:
				rows = executeSingleQueryReturn("SELECT"+tfield+join_str+"LIMIT %s", (songid, limit))
		else:
			rows = executeSingleQueryReturn("SELECT"+tfield+join_str, (songid,))
	else:
		if limit != -1:
			if offset != -1:
				rows = executeSingleQueryReturn("SELECT * FROM tag LIMIT %s,%s", (offset, limit))
			else:
				rows = executeSingleQueryReturn("SELECT * FROM tag LIMIT %s", (limit,))
		else:
			rows = executeSingleQueryReturn("SELECT * FROM tag", ())
	return rows

def isTagExists(tagname):
	return executeSingleQueryReturn("SELECT * FROM tag WHERE name=%s", (tagname,))

def addTag(tagname):
	executeSingleCommand("INSERT INTO tag (name) VALUES(%s)", (tagname,))
	return isTagExists(tagname)

def addTagToSong(tid, sid):
	executeSingleCommand("INSERT INTO taglist (tid, sid) VALUES(%s, %s)", (tid, sid))
