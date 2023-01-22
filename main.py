import requests
from bs4 import BeautifulSoup
import scrapy

# r =  requests.get('https://github.com/joaofxp')

# r.status_code
# r.headers['content-type']
# r.encoding
# html_doc = r.text

# soup = BeautifulSoup(html_doc, 'html.parser')

# soup.select('span[class="repo"]')

# for span in soup.select('span[class="repo"]'):
#     print(span.text)
#     print(span.parent.get('href'))

import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')