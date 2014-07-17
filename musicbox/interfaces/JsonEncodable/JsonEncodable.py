class JsonEncodable:
	def encode(self):
		raise NotImplementedError("class JsonEncodable: Should have implemented encode(self)")
	@staticmethod
	def encodeString(string):
		return "\"" + string + "\""
	@staticmethod
	def encodeInt(integer):
		return str(integer)
	''' table point to default handle method '''
	EncodeTable = {
		"unicode":			encodeString.__func__,
		"int":				encodeInt.__func__
	}
	NotEncodableType = {
		"instancemethod",
		"NoneType"
	}

	@staticmethod
	def encodePair(name, value):
		return name + ":" + value
	'''
		usage:	a default object json-encoder
				encode str and int attr type only
		param:	any object type that will be json-encoded
	'''
	@staticmethod
	def encodeObject(obj):
		result = ""
		for attr in dir(obj):
			# do not encode private var start with '_'
			if attr.startswith("__"): continue

			x = type(getattr(obj, attr)).__name__

			if x in JsonEncodable.NotEncodableType: continue
			if x not in JsonEncodable.EncodeTable:
				print "unknow type " + x
				continue
			result += JsonEncodable.encodePair(JsonEncodable.encodeString(attr), JsonEncodable.EncodeTable[x](getattr(obj, attr))) + ","
		return "{" + result[:-1] + "}"
		
	'''
		param:
			@row:			array of result value
			@fieldNames:	tuple contain field name string
	'''
	@staticmethod
	def encodeSQLRow(row, fieldNames):
		result = ""
		for value,name in zip(row, fieldNames):
			x = type(value).__name__
			if x not in JsonEncodable.NotEncodableType and x in JsonEncodable.EncodeTable:
				result += JsonEncodable.encodePair(JsonEncodable.encodeString(name), JsonEncodable.EncodeTable[x](value)) + ","
		return "{" + result[:-1] + "}"
