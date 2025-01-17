from .base_spider import BaseSpider
from scrapy import Request



class OSSpider(BaseSpider):
    name = "os_spider"
    file_name = "main_result"

    def start_requests(self):
        with open("urls.txt", "r", encoding="utf-8",) as f:
            for url in f:
                yield Request(url=url,callback=self.parse)

    def parse(self, response):
        pass