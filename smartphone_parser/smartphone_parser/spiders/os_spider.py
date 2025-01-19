from .base_spider import BaseSpider
from scrapy import Request
from functools import reduce
from progress.bar import IncrementalBar
from collections import UserDict
import logging
import regex as re
import pandas as pd


class ResultDict(UserDict):

    def __len__(self):
        return sum(self.data.values())

    def __iter__(self):
        self.__keys = list(self.data.keys())
        df = pd.DataFrame(list(self.data.items()), columns=['OS', 'Count'])
        df['Distribution'] = df['Count'] / 100
        df.sort_values(by='Count', inplace=True, ascending=False)
        self.__data_itr = iter(df.iterrows())
        return self

    def __next__(self):
        _, row = next(self.__data_itr)
        return f"{row.OS} - {row.Count} - {row.Distribution}\n"


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
                result = os + " without version designation"
        finally:
            if result:
                self.results[result] = self.results.get(result, 0) + 1
                self.bar.next()
            if len(self.results) >= 100:
                self.logger.error(f"lenresults{len(self.results)}")
                self.crawler.engine.close_spider(self,)
                return
