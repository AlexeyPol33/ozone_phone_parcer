from pathlib import Path

import scrapy


class PhoneSpider(scrapy.Spider):
    name = "phone"
    allowed_domains = ['ozon.ru']
    start_urls = ["https://www.ozon.ru/category/smartfony-15502/?sorting=rating"]

    def parse(self, response):
        pass

    def os_parser(self):
        pass