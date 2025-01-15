from pathlib import Path
from scrapy.selector import Selector
from scrapy import Spider,  signals



class PhoneSpider(Spider):
    name = "phone"
    allowed_domains = ['ozon.ru']
    start_urls = ["https://www.ozon.ru/category/smartfony-15502/?sorting=rating"]

    results = []

    def parse(self, response):
        urls = response.css("div.iw1_23").css("a::attr(href)").extract()
        for url in urls:
            self.results.append("https://www.ozon.ru/" + url)

    def os_parser(self):
        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PhoneSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(str(self.results))
        spider.logger.info("Spider closed")