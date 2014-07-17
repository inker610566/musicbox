from ...interfaces.JsonEncodable.JsonEncodable import JsonEncodable
from ...modules.SQLConf import config
import mysql.connector

class Tag(JsonEncodable):
	def __init__(self, name="", tid=-1):
		if name == "" and tid == -1:
			raise 
		elif name and tid != -1:
			self.name = name
			self.tid = tid
		else:
			ctx = mysql.connector.connect(**config)
			cursor = ctx.cursor()
			if name == "":
				cursor.execute("SELECT * FROM tag WHERE tid=%d", (tid,))
			else:
				cursor.execute("SELECT * FROM tag WHERE name=%s", (name,))
			try:
				(self.tid, self.name) = cursor.next()
			except StopIteration:
				raise TagNotFoundException
			cursor.close()
			ctx.close()
	
	def encode(self):
		#print dict( (x, type(getattr(self, x))) for x in dir(self))
		return JsonEncodable.encodeObject(self)
	
	'''
		param: if offset == -1 then retrieve all
		return: array of song id
	'''
	def getSongList(self, offset=-1, limit=-1):
		ctx = mysql.connector.connect(**config)
		cursor = ctx.cursor()
		query = "SELECT sid FROM taglist WHERE tid=%d"
		if limit != -1 and offset != -1:
			query += "limit %d,%d"
			cursor.excute(query, (self.tid, offset, limit))
		elif limit != -1:
			query += "limit %d"
			cursor.excute(query, (self.tid, limit))
		else:
			cursor.excute(query, (tid,))
		result = [sid for sid in cursor]
		cursor.close()
		ctx.close()
		return result
	
