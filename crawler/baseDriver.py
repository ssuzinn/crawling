from abc import *
from settings import driverPath
from selenium import webdriver
from enum import Enum
from selenium.webdriver.common.keys import Keys


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class FindType(Enum):
    ID = 1
    CSS = 2
    XPATH = 3

    def get_element(self, driver, selector):
        if self == FindType.XPATH:
            return driver.find_element_by_xpath(selector)
        elif self == FindType.CSS:
            return driver.find_element_by_css_selector(selector)
        else:
            return driver.find_element_by_id(selector)

    def get_elements(self, driver, selector):
        if self == FindType.XPATH:
            return driver.find_elements_by_xpath(selector)
        elif self == FindType.CSS:
            return driver.find_elements_by_css_selector(selector)
        else:
            return driver.find_element_by_id(selector)

class BaseDriver(metaclass=ABCMeta):

    baseUrl = ''

    def __init__(self):
        self.driver = webdriver.Chrome(driverPath)
        self.driver.get(self.baseUrl)
        self.driver.implicitly_wait(10)
        self.urls = []


    def submit_keyword(self, selector:str , keyword: str, type: FindType = FindType.XPATH):
        query = type.get_element(driver=self.driver, selector=selector)
        query.send_keys(keyword)
        query.send_keys(Keys.ENTER)

    @abstractmethod
    def run(self, keyword: str):
        pass

    def q(self):
        self.driver.quit()
