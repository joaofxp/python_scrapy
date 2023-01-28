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
    start_urls = ['https://promenacseminovos.com.br/estoque']
    # start_urls = ['https://promenacseminovos.com.br/estoque/?_marca=honda&_paged=2']
    # start_urls = ['https://promenacseminovos.com.br/estoque/?_marca=honda']

    # Default callback method responsible for returning the scraped output and processing it.
    def parse(self, response):
    # XPath expression of all the Quote elements.
        # All quotes belong to CSS attribute class having value 'quote'
        quotes = response.xpath('//*[contains(@class, "elementor-post") and contains(@class, "carros")]')

        # # Loop through the quotes object, to get required elements data.
        for quote in quotes:
            title = quote.xpath('.//div[@id="titulousados"]//h2//a/text()').extract_first()
            km = quote.xpath('.//div/div/div/section/div/div/div/div/div/section[1]/div/div/div/div/div/div/div/h2/text()').extract_first()
            km = km.replace('KM ','')
            ano = quote.xpath('.//div/div/div/section/div/div/div/div/div/section[2]/div/div/div/div/div/div[2]/div/h2/a/text()').extract_first()
            valor = quote.xpath('.//div/div/div/section/div/div/div/div/div/section[2]/div/div/div/div/div/div[4]/div/h2/a/text()').extract_first()
            valor = valor.replace('R$ ')

            yield {
                'Text': title,
                'KM' : km,
                'Ano' : ano,
                'Valor' : valor,
            }

        next_page = response.xpath('//*[contains(text(),"facetwp-page next") and contains(text(),"data-page=")]').get()

        if next_page is not None:
            next_page = re.search('class=..facetwp-page next...data-page=..[0-9]+..',next_page).group(0)
            next_page = re.search('[0-9]+',next_page).group(0)

            next_page ='https://promenacseminovos.com.br/estoque?_paged=' + next_page

            try:
                yield scrapy.Request(url=next_page, callback=self.parse)
            except Exception as e:
                print(e)
