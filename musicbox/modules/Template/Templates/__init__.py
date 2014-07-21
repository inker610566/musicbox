class Template(object):

	def addToParams(self, params):
		pass
	def addToTempList(self, lists):
		lists.append(self.getTemplateFile())
	'''
		return filename
	'''
	def getTemplateFile(self):
		raise NotImplementedError("class Template: Should have implemented __getTemplateFile__(self)")
