import scrapy
from bs4 import BeautifulSoup
from collections import deque


class UICSpider(scrapy.Spider):

    name = "UIC"
    urls = deque()
    done_urls = set()
    i = 0

    def __init__(self, **kwargs):
        super().__init__(name=self.name, **kwargs)
        self.urls.append("https://www.cs.uic.edu/")

    def start_requests(self):

        while self.urls and self.i < 3000:
            url = self.urls.popleft()
            if url not in self.done_urls:
                self.done_urls.add(url)
                self.i += 1
                yield scrapy.Request(url=url, callback=self.parse)
            else:
                continue

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'html.parser')
        yield {
            response.url: soup.prettify()
        }

