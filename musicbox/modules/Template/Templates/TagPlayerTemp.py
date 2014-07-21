from . import Template
'''
	decorator pattern
'''
class TagPlayerTemp(Template):
	def __init__(self, template):
		self.priorName = template.getTemplateFile()
	
	def getTemplateFile(self):
		return "component/tag_player.htmld"
	def getParentFile(self):
		return self.priorName
	def getParentTagName(self):
		return "p_tag_player"


