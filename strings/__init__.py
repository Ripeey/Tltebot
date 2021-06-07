import json, re
class strings:
	def __init__(self):
		with open('./strings/strings.json') as data:
			self.strings = json.load(data)
	
	def key(self,s,lang ="en"):
		if f'*{s}' in self.strings['en']:
			return self.strings[lang][s].format(*self.strings['en'][f'*{s}'])
		else:
			return self.strings[lang][s]
