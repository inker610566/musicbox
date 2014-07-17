# A database interface
from ..SQL import executeSingleQueryReturn

def getSonglist(tagid=0, limit=-1, offset=-1):
	if tagid:
		sfield = " song.* "
		join_str = " FROM taglist INNER JOIN song ON taglist.sid=song.id WHERE tid=%s "
		if limit != -1:
			if offset != -1:
				rows = executeSingleQueryReturn("SELECT"+sfield+join_str+"LIMIT %s,%s", (tagid, offset, limit))
			else:
				rows = executeSingleQueryReturn("SELECT"+sfield+join_str+"LIMIT %s", (tagid, limit))
		else:
			rows = executeSingleQueryReturn("SELECT"+sfield+join_str, (tagid,))
	else:
		if limit != -1:
			if offset != -1:
				rows = executeSingleQueryReturn("SELECT * FROM song LIMIT %s,%s", (offset, limit))
			else:
				rows = executeSingleQueryReturn("SELECT * FROM song LIMIT %s", (limit,))
		else:
			rows = executeSingleQueryReturn("SELECT * FROM song", ())
	return rows
		
