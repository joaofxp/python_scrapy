# scrapy crawl gfg_friendquotes -o friendshipquotes.csv
# Import the required libraries
from urllib.parse import urljoin
import scrapy
import re

# Default class created when we run the "genspider" command


class GfgFriendquotesSpider(scrapy.Spider):
    # Name of the spider as mentioned in the "genspider" command
    name = 'gfg_friendquotes'
    # Domains allowed for scraping, as mentioned in the "genspider" command
    allowed_domains = ['promenacseminovos.com.br']
    # URL(s) to scrape as mentioned in the "genspider" command
    # The scrapy spider, starts making requests, to URLs mentioned here
    # start_urls = ['https://promenacseminovos.com.br/estoque']
    # start_urls = ['https://promenacseminovos.com.br/estoque/?_marca=honda&_paged=2']
    start_urls = ['https://promenacseminovos.com.br/estoque/?_marca=honda']

    # Default callback method responsible for returning the scraped output and processing it.
    def parse(self, response):
    # XPath expression of all the Quote elements.
        # All quotes belong to CSS attribute class having value 'quote'
        next_page = response.xpath('//*[contains(text(),"facetwp-page next") and contains(text(),"data-page=")]').get()
        next_page = re.search('data-page=..[0-9]+',next_page).group(0)
        next_page = re.search('[0-9]+',next_page).group(0)

        # quotes = re.search('[0-9]+',quotes).group(0)

        # quotes = re.search('data-page:[0-9]',quotes).group(0)

        # quotes = response.xpath('//*[contains(@class, "facetwp-page") and contains(@class, "next")]/text()').extract_first()
        yield {'Text':quotes}

        # quotes = response.xpath('//*[contains(@class, "elementor-post") and contains(@class, "carros")]')

        # # Loop through the quotes object, to get required elements data.
        # for quote in quotes:
        #     title = quote.xpath('.//div[@id="titulousados"]//h2//a/text()').extract_first()
        #     km = quote.xpath('.//div/div/div/section/div/div/div/div/div/section[1]/div/div/div/div/div/div/div/h2/text()').extract_first()
        #     ano = quote.xpath('.//div/div/div/section/div/div/div/div/div/section[2]/div/div/div/div/div/div[2]/div/h2/a/text()').extract_first()
        #     valor = quote.xpath('.//div/div/div/section/div/div/div/div/div/section[2]/div/div/div/div/div/div[4]/div/h2/a/text()').extract_first()

        #     yield {
        #         'Text': title,
        #         'KM' : km,
        #         'Ano' : ano,
        #         'Valor' : valor,
        #     }

        if response.xpath('//*[@class="facetwp-page next"]/text()').extract_first() is not None:
            next_page ='https://promenacseminovos.com.br/estoque?_marca=honda&_paged=2'
            try:
                yield scrapy.Request(url=next_page, callback=self.parse)
            except Exception as e:
                print(e)

        # next_page = urljoin(next_page,'2')
        # next_page = urljoin(next_page,response.xpath('.//*[@class="facetwp-page next"]/@data-page').extract_first())

        # if next_page is not None:

        # yield response.follow(next_page, callback=self.parse)
            # yield response.follow('https://promenacseminovos.com.br/estoque?_marca=honda&_paged='.join(next_page), callback=self.parse)

