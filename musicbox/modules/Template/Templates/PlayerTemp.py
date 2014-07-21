class PlayerTemp(Template):
	def __init__(self, template):
		self.priorName = template.__getTemplateFile__()
	
	def getTemplateFile(self):
		return "component/player.htmld"
