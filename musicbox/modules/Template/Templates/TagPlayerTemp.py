from . import Template
'''
	decorator pattern
'''
class TagPlayerTemp(Template):
	def __init__(self, template):
		self.prior = template

	def addToParams(self, params):
		self.prior.addToParams(params)
		params[self.getParentTagName()] = self.getParentFile()

	def addToTempList(self, lists):
		lists.append(self.getTemplateFile())
	
	def getTemplateFile(self):
		return "component/tag_player.htmld"
	def getParentFile(self):
		return self.prior.getTemplateFile()
	def getParentTagName(self):
		return "p_tag_player"


