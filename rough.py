import requests
from bs4 import BeautifulSoup
import collections
import os.path
import os,json
import urllib.request as urllib2
import urllib.parse
from datauri import DataURI
from os import path
import mimetypes

def has_element(queue):
	return len(queue) > 0

def get_next_element(queue):
	if has_element(queue):
		return queue.pop()
	return None, None

def enqueue_element(queue, url, depth):
	queue.appendleft([url, depth])

def get_images(url, soup):
	images = []
	for img in soup.findAll('img'):
		images.append(urllib.parse.urljoin(url, img.get('src')))
	return images

def parse(url):
	reqs = requests.get(url)
	soup = BeautifulSoup(reqs.text, 'html.parser')
	urls = []
	for link in soup.find_all('a'):
		urls.append(urllib.parse.urljoin(url, link.get('href')))
	return urls, get_images(url, soup)

def is_seen(visited, url):
	return True if visited.get(url) else False
def mark_seen(visited, url):
	visited[url] = True
	return visited

def is_image_url(url):
	mimetype,encoding = mimetypes.guess_type(url)
    if mimetype and mimetype.startswith('image'):
    	return True

def write_to_file(images, depth, source_url):
	data = {"results": []}
	cwd = os.getcwd()
	filename = cwd + "/results.json"
	if path.exists(filename):
		with open(filename) as f:
			data = json.load(f)
	for img in images:
		data["results"].append({
			"imageUrl":img,
			"sourceUrl": source_url,
			"depth": depth
			})
	with open(filename, 'w') as f:
		json.dump(data, f)

def scrape(start_url, max_depth):
	queue = collections.deque()
	queue.appendleft([start_url, 0])
	visited = {}
	mark_seen(visited, start_url)
	while has_element(queue):
		url, depth = get_next_element(queue)
		urls, images = parse(url)
		print(urls)
		print("images", images, depth)
		write_to_file(images, depth, url)
		for url in urls:
			if not is_seen(visited, url) and depth + 1 <= max_depth:
				enqueue_element(queue, url, depth + 1)
				mark_seen(visited, url)
scrape("https://css-tricks.com/examples/DataURIs/", 2)
