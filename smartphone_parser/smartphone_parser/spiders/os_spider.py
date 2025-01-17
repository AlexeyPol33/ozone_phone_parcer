from .base_spider import BaseSpider
from scrapy import Request
from scrapy.selector import Selector
import regex as re


class OSSpider(BaseSpider):
    name = "os_spider"
    file_name = "main_result"
    scroll = 3000
    results = []

    def start_requests(self):

        with open("urls.txt", "r", encoding="utf-8",) as f:
            for url in f:
                yield Request(url=url,callback=self.parse)

    def parse(self, response):
        os = response.xpath('//*[@id="section-characteristics"]').get()
        version = response.xpath('//*[@id="section-characteristics"]/div[2]/div[7]/div[3]/dl[2]/dd').get()
        self.results.append(str(os) + "\n")
