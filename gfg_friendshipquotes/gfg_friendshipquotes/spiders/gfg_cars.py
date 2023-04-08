# scrapy crawl gfg_friendquotes -o friendshipquotes.csv
from urllib.parse import urljoin
import scrapy
import re

carStores = [
    {
          "titulo":"promenac"
        , "domain":"promenacseminovos.com.br"
        , "urlCrawl":"https://promenacseminovos.com.br/estoque"
        , "urlNext":"https://promenacseminovos.com.br/estoque?_paged="
        , "buttonNextPage":'//*[contains(text(),"facetwp-page next") and contains(text(),"data-page=")]'
        , "dadosCarro" : {
              "listaCarrosXPath":'//*[contains(@class, "elementor-post") and contains(@class, "carros")]'
            , "tituloCarroXPath":'.//div[@id="titulousados"]//h2//a/text()'
            , "kmXPath":'.//div/div/div/section/div/div/div/div/div/section[1]/div/div/div/div/div/div/div/h2/text()'
            , "anoXPath":'.//div/div/div/section/div/div/div/div/div/section[2]/div/div/div/div/div/div[2]/div/h2/a/text()'
            , "valorXPath":'.//div/div/div/section/div/div/div/div/div/section[2]/div/div/div/div/div/div[4]/div/h2/a/text()'
        }
    }
]

carIndex = 0

def carregarDadosLojaCarro():
    carStore = {}
    carStore['listaCarrosXPath'] = carStores[carIndex]["dadosCarro"]["listaCarrosXPath"]
    carStore['tituloCarroXPath'] = carStores[carIndex]["dadosCarro"]["tituloCarroXPath"]
    carStore['kmXPath'] = carStores[carIndex]["dadosCarro"]["kmXPath"]
    carStore['anoXPath'] = carStores[carIndex]["dadosCarro"]["anoXPath"]
    carStore['valorXPath'] = carStores[carIndex]["dadosCarro"]["valorXPath"]
    carStore['buttonNextPage'] = carStores[carIndex]['buttonNextPage']
    carStore['urlNext'] = carStores[carIndex]['urlNext']
    return carStore

class GfgCarsSpider(scrapy.Spider):
    name = 'gfg_cars'
    allowed_domains = []
    start_urls = []

    for carStore in carStores:
        allowed_domains.append(carStore['domain'])
        start_urls.append(carStore['urlCrawl'])

    def parse(self, response):
        carsArray = {}

        carStore = carregarDadosLojaCarro()
        carsArray = response.xpath(carStore['listaCarrosXPath'])

        for car in carsArray:
            title = car.xpath(carStore['tituloCarroXPath']).extract_first()
            km = car.xpath(carStore['kmXPath']).extract_first()
            km = km.replace('KM ','')
            ano = car.xpath(carStore['anoXPath']).extract_first()
            valor = car.xpath(carStore['valorXPath']).extract_first()
            valor = valor.replace('R$ ','')

            if int(km) < 50000:
                yield {
                    'Text': title,
                    'KM' : km,
                    'Ano' : ano,
                    'Valor' : valor,
                }

        next_page = response.xpath(carStore['buttonNextPage']).get()

        if next_page is not None:
            next_page = re.search('class=..facetwp-page next...data-page=..[0-9]+..',next_page).group(0)
            next_page = re.search('[0-9]+',next_page).group(0)

            next_page = carStore['urlNext'] + next_page

            try:
                yield scrapy.Request(url=next_page, callback=self.parse)
            except Exception as e:
                print(e)


