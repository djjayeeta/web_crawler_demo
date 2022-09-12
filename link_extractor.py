import urllib.parse
import validators

class BaseLinkExtractor:
	def __init__(self):
		pass

	def extract_links(self, soup, req):
		urls = []
		for link in soup.find_all('a'):
			urls.append(urllib.parse.urljoin(req.url, link.get('href')))
		return set(urls)

	def get_valid_invalid_links(self, soup, req):
		urls = self.extract_links(soup, req)
		valid_urls = []
		invalid_urls = []
		for url in urls:
			if validators.url(url):
				valid_urls.append(url)
			else:
				invalid_urls.append([url, validators.url(url)])
		return valid_urls, invalid_urls



class ImageLinkExtractor(BaseLinkExtractor):
	def __init__(self):
		pass

	def extract_links(self, soup, req):
		urls = []
		for link in soup.findAll('img'):
			urls.append(urllib.parse.urljoin(req.url, link.get('src')))
		return set(urls)
