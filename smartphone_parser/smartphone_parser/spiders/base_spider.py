from typing import Iterable
from pathlib import Path
from scrapy.selector import Selector
from scrapy import Spider,  signals



class BaseSpider(Spider):
    name: str
    file_name: str | None = None
    start_urls: Iterable
    results: Iterable[str]

    allowed_domains = ['ozon.ru']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BaseSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider:Spider):
        if self.file_name:
            with open(f"{self.file_name}.txt", "w", encoding="utf-8") as f:
                f.writelines(self.results)
        spider.logger.info(f"The spider completed its work with results: {len(self.results)}")