from flask import render_template
'''
	it load 2 kinds of template:
		header_templates:
			it will be inserted before component template
		component_templates:
			it will be inserted after head template
'''
class TemplateManager:
	def __init__(self):
		self.header_templates = []
		self.component_templates = []
		self.params = dict()
	
	def loadHeadTemplate(self, template):
		self.header_templates.append(template.getTemplateFile())
		p = template.getParentTagName()
		if p:
			self.params[p] = template.getParentFile()

	def loadComponentTemplate(self, template):
		self.component_templates.append(template.getTemplateFile())
		p = template.getParentTagName()
		if p:
			self.params[p] = template.getParentFile()

	def getHtml(self):
		return render_template(
			"test.htmld",
			header_templates=self.header_templates,
			component_templates=self.component_templates,
			**self.params)
