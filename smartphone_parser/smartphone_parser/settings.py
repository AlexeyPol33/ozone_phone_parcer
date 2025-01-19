import logging
import logging.config
from selenium.webdriver.remote.remote_connection import LOGGER as webdriver_logger
from urllib3.connectionpool import log as urllib3_logger
from scrapy.core.engine import logger as scrapy_logger

BOT_NAME = "smartphone_parser"

SPIDER_MODULES = ["smartphone_parser.spiders"]
NEWSPIDER_MODULE = "smartphone_parser.spiders"

LOG_LEVEL = logging.ERROR
scrapy_logger.setLevel(logging.INFO)
webdriver_logger.setLevel(logging.NOTSET)
urllib3_logger.setLevel(logging.INFO)

ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
   "smartphone_parser.middlewares.SmartphoneParserDownloaderMiddleware": 543,
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
