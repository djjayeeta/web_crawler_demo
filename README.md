## About The Project

# Overview
Lighweight single threaded web crawler.

Given a `start_url` and a `max_depth` it can crawl html pages and extract valid images link for each page starting from `start_url` till a `max_depth` and stores in a output file `results.json` in the current directory.

Ex. Depth 0 means only the url itself(if its a image), Depth 1 means any images inside the source url will be extracted and stored in the output file.


# Architechuture of the crawler

![Architecture](https://github.com/djjayeeta/web_crawler_demo/blob/master/architechture.png?raw=true) 

## Steps to run

# Prequisites

1. Install [Python 3.4+](https://www.python.org/downloads/release/python-330/) 
2. Install [pip 3](https://www.activestate.com/resources/quick-reads/how-to-install-and-use-pip3/)
3. Install [virtual env](http://timsherratt.org/digital-heritage-handbook/docs/python-pip-virtualenv/)

# Commands to run

1. Setup 

```
virtualenv -p python3 crawler_env
source crawler_env/bin/activate
git clone https://github.com/djjayeeta/web_crawler_demo.git
cd web_crawler_demo
pip install -r requirements.txt
```
2. crawl web page

```
python crawler.py -s https://smiles.ai/ -d 2
```

# Output

The output is stored in the format
```
{
	results: [
		{
			imageUrl: string,
			sourceUrl: string // the page url this image was found on
			depth: number // the depth of the source at which this image was found on
		}
	]
}
```

1. All combinations of `imageUrl` and `sourceUrl` are stored in the output
2. If `imageUrl` and `sourceUrl` are seen at multiple `depth` then only the first `depth` will be recorded.

# Not covered
1. Non html pages like, xml parsing
2. Infinite scroll pages
3. Pages which has ajax content, ex. we need to click some buttons to load more content 
4. Storing of state of the crawler in case of crashes
