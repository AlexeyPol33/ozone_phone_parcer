from .base_spider import BaseSpider
from scrapy import Request
from scrapy.selector import Selector
from functools import reduce
from progress.bar import IncrementalBar
import regex as re


class OSSpider(BaseSpider):
    name = "os_spider"
    file_name = "main_result"
    scroll = 4000
    bar = IncrementalBar('Data collection in progress',max=100)
    results = []

    def start_requests(self):

        with open("urls.txt", "r", encoding="utf-8",) as f:
            for url in f:
                yield Request(url=url,callback=self.parse)

    def parse(self, response):
        self.bar.next()
        characteristics = response.xpath('//*[@id="layoutPage"]/div[1]/div[6]/div/div[1]/div[2]/div[2]/div/div/div[3]')
        os = characteristics.re(r"(Android|iOS|Windows|Linux|macOS)")
        try:
            version = characteristics.re(r'Версия(.*?)</div>')
            version = map(lambda txt: re.findall(r">([^<]+)<", txt),version)
            version = reduce(lambda x, y: x+y,version)
            version = [v for v in version if bool(re.search(r'\d', v))]
            if version:
                self.results.append(str(version) + "\n")
            else:
                raise
        except:
            if os:
                self.results.append(str(list(os)) + "\n")