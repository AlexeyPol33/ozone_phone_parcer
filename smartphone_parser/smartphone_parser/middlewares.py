from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
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

        log = logging.getLogger("middleware.DriverSingleton.scroll")
        try:
            position = 0
            while y >= position:
                scroll_height = self.execute_script("return document.body.scrollHeight;")
                if scroll_height < y:
                    self.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    position = scroll_height
                    WebDriverWait(self,5).until_not(lambda d: d.execute_script("return document.body.scrollHeight;") <= scroll_height)
                else:
                    self.execute_script(f"window.scrollTo(0, {y})")
                    position = scroll_height
        except TimeoutException:
            log.warning(msg="Ending scrolling with timeout")
        except Exception as e:
            log.error(msg=f"Unexpected exception:{repr(e)}")


class SmartphoneParserDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):

        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        driver = DriverSingleton()
        driver.get(request.url)
        WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.ID, "__ozon")))

        if spider.scroll:
            driver.scroll(spider.scroll)

        return HtmlResponse(
            url=driver.current_url,
            body=str.encode(driver.page_source),
            encoding='utf-8',
            request=request
            )

    def process_response(self, request, response, spider):

        DriverSingleton().close()
        return response

    def spider_opened(self, spider):

        spider.logger.info("Spider opened: %s" % spider.name)
