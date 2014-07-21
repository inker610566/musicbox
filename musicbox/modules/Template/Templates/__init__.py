class Template:
	'''
		return filename
	'''
	def getTemplateFile(self):
		raise NotImplementedError("class Template: Should have implemented __getTemplateFile__(self)")
	'''
		return parent filename
	'''
	def getParentFile(self):
		return None

	'''
		a symbol string defined in Jinja represent its parent
		if no template have no parent, None is returned
	'''
	def getParentTagName(self):
		return None

