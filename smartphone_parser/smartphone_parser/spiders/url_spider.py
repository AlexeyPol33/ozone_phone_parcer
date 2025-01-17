from .base_spider import BaseSpider

class URLSpider(BaseSpider):
    name = "url_spider"
    file_name = "urls"
    start_urls = ["https://www.ozon.ru/category/smartfony-15502/?sorting=rating"]

    results = []

    def parse(self, response):
        urls = response.css("div.wi1_23").css("a::attr(href)").extract()
        self.results = ["https://www.ozon.ru" + f"{url}\n" for url in urls][:100]