from datetime import datetime
from enum import Enum
from abc import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from settings import driverPath


class FindType(Enum):
    ID = 1
    XPATH = 2
    CSS = 3

    def get_element(self, driver, selector):
        if self == FindType.ID:
            return driver.find_element_by_id(selector)
        if self == FindType.XPATH:
            return driver.find_element_by_xpath(selector)
        if self == FindType.CSS:
            return driver.find_element_by_css_selector(selector)

    def get_elements(self, driver, selector):
        if self == FindType.XPATH:
            return driver.find_elements_by_xpath(selector)
        if self == FindType.CSS:
            return driver.find_elements_by_css_selector(selector)


class BaseDriver(metaclass=ABCMeta):
    baseurl = ''
    url_list = []
    title = ''
    publish_date = datetime.now()
    body = ''
    contents = []

    def __init__(self):
        self.driver = webdriver.Chrome(driverPath)
        self.driver.get(self.baseurl)
        self.driver.implicitly_wait(3)

    def submit_keyword(self, selector, keyword, type: FindType = FindType.XPATH):
        query = type.get_element(driver=self.driver, selector=selector)
        query.send_keys(keyword)
        query.send_keys(Keys.ENTER)

    def q(self):
        self.driver.quit()

    @abstractmethod
    def run(self, keyword: str):
        pass
