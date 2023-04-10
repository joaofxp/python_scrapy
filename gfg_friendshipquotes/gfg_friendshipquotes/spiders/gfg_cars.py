# scrapy crawl gfg_friendquotes -o friendshipquotes.csv
from urllib.parse import urljoin
import scrapy
import re

carStores = [
    {
          "storeName":"ccv"
        , "domain":"ccvcatarinensechevrolet.com.br"
        , "urlCrawl":"https://www.ccvcatarinensechevrolet.com.br/seminovos?condicao=seminovo&marca=chevrolet,fiat,hyundai,volkswagen&ano=2022,2021,2020,2019,2018&preco=r$%2040.000%20a%20r$%2060.000,r$%2060.000%20a%20r$%2080.000&quilometragem=inferior%20a%2020.000,20.000%20a%2040.000,40.000%20a%2060.000"
        , "urlNext": None
        , "buttonNextPage": None
        , "dadosCarro" : {
              "listaCarrosXPath":'//*[contains(@class,"vehicle-tile ng-star-inserted")]'
            , "tituloCarroXPath":'.//p[@class="inventory-title"]/text()'
            , "kmXPath":None
            , "anoXPath":'.//p[@class="inventory-title"]/text()'
            , "valorXPath":'.//p[@class="sub-price"]/text()'
        }
    }
    ,
    {
          "storeName":"globo"
        , "domain":"grupoglobo.com.br"
        , "urlCrawl":"https://www.grupoglobo.com.br/seminovos"
        , "urlNext": None
        , "buttonNextPage": None
        , "dadosCarro" : {
              "listaCarrosXPath":'//*[contains(@class, "list_semi") and contains(@class, "col-xs-12 list_semi2")]//div[@class="list_semi" and (contains(.,"Itajaí") or contains(.,"Balneário Camboriú"))]'
            , "tituloCarroXPath":'.//div[@class="titl_list_semi text_azul2"]//a/text()'
            , "kmXPath":None
            , "anoXPath":'.//div[3]//a//span/text()'
            , "valorXPath":'.//div[@class="valr_list_semi font_bold"]//a/text()[2]'
        }
    }
    ,
    {
          "storeName":"promenac"
        , "domain":"promenacseminovos.com.br"
        , "urlCrawl":"https://promenacseminovos.com.br/estoque"
        , "urlNext":"https://promenacseminovos.com.br/estoque?_paged="
        , "buttonNextPage": '//*[contains(text(),"facetwp-page next") and contains(text(),"data-page=")]'
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
    global carIndex

    carStore = {}
    carStore['listaCarrosXPath'] = carStores[carIndex]["dadosCarro"]["listaCarrosXPath"]
    carStore['tituloCarroXPath'] = carStores[carIndex]["dadosCarro"]["tituloCarroXPath"]
    carStore['kmXPath'] = carStores[carIndex]["dadosCarro"]["kmXPath"]
    carStore['anoXPath'] = carStores[carIndex]["dadosCarro"]["anoXPath"]
    carStore['valorXPath'] = carStores[carIndex]["dadosCarro"]["valorXPath"]
    carStore['buttonNextPage'] = carStores[carIndex]['buttonNextPage'] if carStores[carIndex]['buttonNextPage'] else None
    carStore['urlNext'] = carStores[carIndex]['urlNext']
    carStore['storeName'] = carStores[carIndex]['storeName']

    return carStore

def temProximaLoja():
    global carIndex

    if len(carStores) > carIndex + 1:
        carIndex += 1
        return True
    else:
        return False
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
            title = car.xpath(carStore['tituloCarroXPath']).extract_first().strip()
            title = re.sub('[0-9]+','',title)

            km = car.xpath(carStore['kmXPath']).extract_first() if carStore['kmXPath'] else ''
            km = km.replace('KM ','').strip()

            ano = car.xpath(carStore['anoXPath']).extract_first()
            ano = re.findall(r'\d+', ano)

            valor = car.xpath(carStore['valorXPath']).extract_first()
            valor = re.findall('[0-9.,]+',valor)

            storeName = carStore['storeName']

            km = None if km == '' else km

            if km is not None and int(km) < 60000:
                yield {
                    'Text': title,
                    'Ano' : ano,
                    'Valor' : valor,
                    'Concessionaria': storeName,
                    'KM' : km,
                }
            else:
                yield {
                    'Text': title,
                    'Ano' : ano,
                    'Valor' : valor,
                    'Concessionaria': storeName,
                }

        next_page = response.xpath(carStore['buttonNextPage']).get() if carStore['buttonNextPage'] else None

        if next_page is not None:
            # tratativa para promenac, pois carregam o botao em uma tag script e o XPath não consegue extrair de dentro de um string de uma vez só
            if(carStore['storeName'] == 'promenac'):
                next_page = re.search('class=..facetwp-page next...data-page=..[0-9]+..',next_page).group(0)
                next_page = re.search('[0-9]+',next_page).group(0)

            next_page = carStore['urlNext'] + next_page

            try:
                yield scrapy.Request(url=next_page, callback=self.parse)
            except Exception as e:
                print(e)
        else:
            if temProximaLoja() is True:
                global carIndex
                print('novoIndex',carIndex)
                self.parse()


