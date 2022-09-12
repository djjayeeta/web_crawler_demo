import requests
from requests.adapters import HTTPAdapter, Retry

class Request:
	def __init__(self, url, retries = 3):
		self.retries = retries
		self.url = url

	def get_response(self):
		raise NotImplementedError

	def get_response_content_type(self, resp):
		raise NotImplementedError

class HttpRequest(Request):
	def __init__(self, url, retries = 3):
		self.retries = retries
		self.url = url
		session = requests.Session()
		adapter = HTTPAdapter(max_retries=Retry(total=retries, backoff_factor=0.1, allowed_methods=None, status_forcelist=[429, 500, 502, 503, 504]))
		session.mount("http://", adapter)
		session.mount("https://", adapter)
		self.session = session

	def get_response(self):
		try:
			resp = self.session.get(self.url, timeout=5)
			resp.close()
		except Exception as e:
			return None, str(e)
		return resp, None if resp.ok else None, resp.reason

	def get_response_content_type(self, resp):
		if resp is not None and resp.ok:
			return resp.headers.get("Content-Type")
		return None