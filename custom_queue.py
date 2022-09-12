import collections

class CustomQueue:
	def __init__(self):
		self.queue = collections.deque()
		self.enqueue_duplicate = False

	def has_element(self):
		return len(self.queue) > 0

	def get_next_element(self):
		if self.has_element():
			return self.queue.pop()
		return None

	def enqueue_element(self, element ):
		self.queue.appendleft(element)