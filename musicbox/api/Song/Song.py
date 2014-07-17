from ...interfaces.JsonEncodable.JsonEncodable import JsonEncodable

class Song(JsonEncodable):
	def __init__(self, name, location=u"", image=u""):
		self.name = name
		self.location = location
		self.image = image
		
	def encode(self):
		#print dict( (x, type(getattr(self, x))) for x in dir(self))
		return JsonEncodable.encodeObject(self)

	def 
