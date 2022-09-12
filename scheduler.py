from custom_queue import CustomQueue
from de_dup_filter import DeDupFilter
from parser import Parser
from dataclasses import dataclass

@dataclass
class Settings:
	max_depth: int
	max_retries: int

class Scheduler:
	def __init__(self, max_depth, output):
		self.queue = CustomQueue()
		self.dedup_filter = DeDupFilter()
		settings = Settings(max_depth, 1)
		self.parser = Parser(self.dedup_filter, output, settings, self.queue)

	def has_pending_requests(self):
		return self.queue.has_element()

	def schedule_request(self):
		item = self.queue.get_next_element()
		self.parser.parse(item)
		