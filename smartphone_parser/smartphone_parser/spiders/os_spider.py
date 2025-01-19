from .base_spider import BaseSpider
from scrapy import Request
from functools import reduce
from progress.bar import IncrementalBar
from collections import UserDict
import regex as re


class ResultDict(UserDict):

    def __len__(self):
        return sum(self.data.values())

    def __iter__(self):
        self.__keys = list(self.data.keys())
        return self

    def __next__(self):
        if not self.__keys:
            raise StopIteration
        high_value_index = 0
        for key_i in range(len(self.__keys)):
            if self.data[self.__keys[key_i]] > self.data[self.__keys[high_value_index]]:
                high_value_index = key_i
        os = self.__keys.pop(high_value_index)
        return f"{os} - {self.data[os]}\n"


class OSSpider(BaseSpider):
    name = "os_spider"
    file_name = "main_result"
    scroll = 4000
    bar = IncrementalBar('Data collection in progress', max=100)
    results = ResultDict()

    def start_requests(self):

        with open("urls.txt", "r", encoding="utf-8",) as f:
            for url in f:
                yield Request(url=url, callback=self.parse)

    def parse(self, response):

        result: str | None = None
        if len(self.results) > 100:
            return
        characteristics = response.xpath('//*[@id="layoutPage"]/div[1]/div[6]/div/div[1]/div[2]/div[2]/div/div/div[3]')
        os = characteristics.re(r"(Android|iOS|Windows|Linux|macOS)")
        os = list(os)
        try:
            version = characteristics.re(r'Версия(.*?)</div>')
            version = map(lambda txt: re.findall(r">([^<]+)<", txt), version)
            version = reduce(lambda x, y: x + y, version)
            version = [v for v in version if bool(re.search(r'\d', v))]
            if version:
                version = version.pop()
                result = version
            else:
                raise
        except Exception:
            if os:
                os = os.pop()
                result = os + "without version designation"
        finally:
            if result:
                self.results[result] = self.results.get(result, 0) + 1
                self.bar.next()
