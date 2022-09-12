import custom_request


class Item:
	def __init__(self, url, depth, source_url=None):
		self.url = url
		self.depth = depth
		self.source_url = source_url
		self.current_try = 0
		self.req_class = getattr(custom_request,'HttpRequest')

	def to_request(self):
		return self.req_class(self.url)