import os.path
import os,json
from os import path

class Output:
	def __init__(self, filename):
		cwd = os.getcwd()
		self.filepath = cwd + "/" + filename
		data = {"results": []}
		with open(filename, 'w') as f:
			json.dump(data, f)

	def flush(self, images_to_write):
		data = {}
		with open(self.filepath) as f:
			data = json.load(f)
		for img in images_to_write:
			data["results"].append({
				"imageUrl":img.url,
				"sourceUrl": img.source_url,
				"depth": img.depth
				})
		with open(self.filepath, 'w') as f:
			json.dump(data, f)