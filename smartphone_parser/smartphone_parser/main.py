from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.phone_spider import PhoneSpider


settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(PhoneSpider)
process.start()