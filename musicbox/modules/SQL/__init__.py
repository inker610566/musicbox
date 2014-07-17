from ..SQLConf import config
import mysql.connector

def executeSingleQueryReturn(stmt, param):
	@executeSingleQuery
	def query(cursor):
		return [row for row in cursor]
	return query(stmt, param)

def executeSingleQuery(handle_cursor):
	def callQuery(stmt, param):
		ctx = mysql.connector.connect(**config)
		cursor = ctx.cursor()
		cursor.execute(stmt, param)
		res = handle_cursor(cursor)
		cursor.close()
		ctx.close()
		return res
	return callQuery

def executeSingleCommand(stmt, param):
	ctx = mysql.connector.connect(**config)
	cursor = ctx.cursor()
	cursor.execute(stmt, param)
	ctx.commit()
	cursor.close()
	ctx.close()
	
