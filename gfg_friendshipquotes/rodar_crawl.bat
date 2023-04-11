IF EXIST cars.csv DEL /F cars.csv;
scrapy crawl gfg_cars -o cars.csv