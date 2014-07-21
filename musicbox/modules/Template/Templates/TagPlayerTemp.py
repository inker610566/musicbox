'''
	decorator pattern
'''
class TagPlayerTemp(Template):
	def __init__(self, template):
		self.priorName = template.__getTemplateFile__()
	
	def getTemplateFile(self):
		return "header/tag_player.htmld"
	def getParentFile(self):
		return self.priorName
	def getParentFile(self):
		return "p_tag_player"


