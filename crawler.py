from output import Output
from scheduler import Scheduler
from item import Item
import click
import validators

class Crawler:
	def __init__(self, start_url, max_depth):
		"""
		Initialises the crawler
		:param start_url: a string which represents the starting url of the crawler
		:type start_url: :class:`str`
		:param max_depth: max_depth till which we will look for urls, 
		ex.max_depth 0 implies only till start_url
		max_depth 1 implies crawl all links in the start_url
		:type max_depth: :class:`int`
		"""
		output = Output("results.json")
		self.scheduler = Scheduler(max_depth, output)
		self.start_url = start_url

	def crawl(self):
		# push start url into queue
		item = Item(self.start_url, 0)
		self.scheduler.queue.enqueue_element(item)
		self.scheduler.dedup_filter.mark_seen(item)
		# scheduling loop
		while self.scheduler.has_pending_requests():
			self.scheduler.schedule_request()


def validate_start_url(ctx, param, value):
	if validators.url(value):
		return value
	else:
		raise click.BadParameter("Must be a valid url")

def validate_max_depth(ctx, param, value):
	if isinstance(value, int) and value >= 0:
		return value
	else:
		raise click.BadParameter("Must be a valid int greater than or equal to 0")

@click.command()
@click.option("-s", "--start_url", type=str, required=True, callback=validate_start_url,
		help="Must be a valid url")
@click.option("-d", "--max_depth", type=int, required=True, callback=validate_max_depth,
			  help="Must be a valid int greater than or equal to 0")

def cli(start_url, max_depth):
	c = Crawler(start_url, max_depth)
	c.crawl()

if __name__ == '__main__':
	cli()

