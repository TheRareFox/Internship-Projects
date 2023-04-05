'''
This is a web crawler for Brahm Center page
As we are removing any mentions of ACP, this web crawler will go through all possible web paths on the website
and return the list of all the urls with mentions of ACP so that we can remove them
'''

import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

Searching = ['advance care planning','Advance Care Planning','acp']



logging.basicConfig(
  format='%(asctime)s %(levelname)s:%(message)s',
  level=logging.INFO)

class Crawler:

  def __init__(self, urls=[]):
    self.visited_urls = []
    self.urls_to_visit = urls
    self.found_urls = []

  def download_url(self, url):
    return requests.get(url, headers=HEADERS).text


  def get_linked_urls(self, url, html):
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    notFound = True
    for i in Searching:
      if(notFound):
        a = soup(string = i)
        if a:
          print(a)
          notFound = False
          self.found_urls.append(url)
          #print(url)
  
    for link in soup.find_all('a'):
      path = link.get('href')
      if path and path.startswith('/'):
        path = urljoin(url, path)
      yield path

  def add_url_to_visit(self, url):
    if url not in self.visited_urls and url not in self.urls_to_visit:
        self.urls_to_visit.append(url)

  def crawl(self, url):
    html = self.download_url(url)
    for url in self.get_linked_urls(url, html):
        self.add_url_to_visit(url)

  def run(self):
    while self.urls_to_visit:
      url = self.urls_to_visit.pop(0)
      if not url:
        continue
      self.visited_urls.append(url)
      try:
        if(url.startswith('https://brahmcentre.com/')):
          logging.info(f'Crawling: {url}')
          self.crawl(url)          
      except:
        logging.exception(f'Failed to crawl: {url}')
        print(self.found_urls)
    print(self.found_urls)

if __name__ == '__main__':
    Crawler(urls=['https://brahmcentre.com/']).run()
