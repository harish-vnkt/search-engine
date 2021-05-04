import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class UICSpider(scrapy.Spider):

    name = "UIC"
    start_urls = ["https://www.cs.uic.edu/"]
    allowed_domains = ["uic.edu"]
    done_urls = set()
    i = 0
    # download_delay = 2.0

    def parse(self, response):

        if self.i < 4000 and "uic.edu" in response.url and response.url not in self.done_urls:

            self.done_urls.add(response.url)

            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            outgoing_urls = []

            for link in links:
                url = link.get("href")
                url = urljoin(response.url, url)
                if url and "uic.edu" in url and "@" not in url:
                    outgoing_urls.append(url)

            self.i += 1

            yield {
                "url": response.url,
                "soup": soup.prettify(),
                "outgoing_urls": outgoing_urls
            }

            yield from response.follow_all(outgoing_urls, callback=self.parse)



