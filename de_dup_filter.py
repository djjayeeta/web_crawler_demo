class DeDupFilter:
	def __init__(self):
		self.visited = {}

	def is_seen(self, item):
		return True if self.visited.get(item.url) else False
	
	def mark_seen(self, item):
		self.visited[item.url] = True
		return True