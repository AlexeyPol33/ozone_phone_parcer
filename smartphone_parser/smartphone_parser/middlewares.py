from scrapy import signals
from scrapy.http import HtmlResponse
from itemadapter import is_item, ItemAdapter
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from abc import ABCMeta
import time
import logging


class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DriverSingleton(webdriver.Chrome,metaclass=SingletonMeta):

    @property
    def __options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        #options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        return options

    @property
    def __stealth_parameters(self):
        ua = UserAgent(browsers='chrome', os='windows', platforms='pc').random
        return {
                "languages":["en-US", "en"],
                "user_agent":ua,
                "vendor":"Google Inc.",
                "platform":"Win32",
                "webgl_vendor":"Intel Inc.",
                "renderer":"Intel Iris OpenGL Engine",
                "fix_hairline":True,
        }

    def __init__(self):
        options = self.__options
        service = Service(ChromeDriverManager().install())
        stealth_parameters = self.__stealth_parameters
        super().__init__(options, service, keep_alive= True)
        stealth(self,**stealth_parameters)

    def scroll(self, y:int) -> None:
        """Scrolls the page to position y or end"""

        try:
            position = 0
            while y >= position:
                scroll_height = self.execute_script('return document.body.scrollHeight;')
                if scroll_height < y:
                    self.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    position = scroll_height
                    WebDriverWait(self,5).until_not(lambda d: d.execute_script('return document.body.scrollHeight;') <= scroll_height)
                else:
                    self.execute_script("window.scrollTo(0, y)")
                    position = scroll_height
        except Exception as e:
            log = logging.getLogger("middleware.DriverSingleton.scroll")
            log.error(msg=repr(e))

class SmartphoneParserSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SmartphoneParserDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        driver = DriverSingleton()
        driver.get(request.url)
        WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.ID, "__ozon")))
        scrols = driver.scroll(10000)
        body = str.encode(driver.page_source)
        url = driver.current_url
        driver.close()
        return HtmlResponse(
            url,
            body=body,
            encoding='utf-8',
            request=request
            )

    def process_response(self, request, response, spider):

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
