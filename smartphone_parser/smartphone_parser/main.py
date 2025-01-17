from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from smartphone_parser.smartphone_parser.spiders.url_spider import URLSpider


settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(URLSpider)
process.start()