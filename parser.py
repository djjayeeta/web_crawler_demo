from item import Item
from bs4 import BeautifulSoup
from link_extractor import BaseLinkExtractor, ImageLinkExtractor
import lxml
import logging

logging.basicConfig(level=logging.WARNING, format='%(name)s - %(levelname)s - %(message)s')

class Parser:
	def __init__(self, dedup_filter, output, settings, queue):
		self.dedup_filter = dedup_filter
		self.settings = settings
		self.queue = queue
		self.output = output
		self.imageLinkExtractor = ImageLinkExtractor()
		self.linkExtractor = BaseLinkExtractor()

	def parse(self, item):
		req = item.to_request()
		r = req.get_response()
		resp, reason = r[0], r[1]

		if not resp:
			if item.current_try + 1 < self.settings.max_retries:
				logging.warn('The resp is returned None due to %s at depth %s from url %s pushing again to queue', reason, item.depth, item.url)
				self.queue.enqueue_element(item)
			else:
				logging.error('The resp is returned None due to %s at depth %s from url %s ignoring item', reason, item.depth, item.url)
			return

		images_to_write = []
		content_type = req.get_response_content_type(resp)
		if content_type is not None and content_type.startswith("image"):
			images_to_write.append(item)
		elif item.depth < self.settings.max_depth:
			soup = BeautifulSoup(resp.text, 'html.parser')
			valid_images, invalid_images = self.imageLinkExtractor.get_valid_invalid_links(soup, req)
			valid_images = set(valid_images)
			if len(invalid_images) > 0:
				logging.warn('The invalid_images are %s in depth %s from url %s', [u[0] for u in invalid_images], item.depth, item.url)
			for img in valid_images:
				images_to_write.append(Item(img, item.depth + 1, item.url))
			valid_urls, invalid_urls = self.linkExtractor.get_valid_invalid_links(soup, req)
			if len(invalid_urls) > 0:
				logging.warn('The invalid_images are %s in depth %s from url %s', [u[0] for u in invalid_urls], item.depth, item.url)
			for url in valid_urls:
				item = Item(url, item.depth + 1, item.url)
				if url not in valid_images and not self.dedup_filter.is_seen(item):
					self.queue.enqueue_element(item)
					self.dedup_filter.mark_seen(item)
		self.output.flush(images_to_write)
		