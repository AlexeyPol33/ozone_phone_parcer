from .base_spider import BaseSpider
from progress.spinner import LineSpinner


class URLSpider(BaseSpider):
    name = "url_spider"
    file_name = "urls"
    bar = LineSpinner('URLS collection in progress ')
    scroll = 14000
    start_urls = ["https://www.ozon.ru/category/smartfony-15502/?sorting=rating"]

    results = []

    def parse(self, response):
        self.bar.next()
        urls = response.css("div.wi1_23").css("a::attr(href)").extract()
        self.bar.next()
        self.results = ["https://www.ozon.ru" + f"{url}\n" for url in urls]
        self.bar.next()
        self.results = list(set(self.results))[:100]
        self.bar.next()