import re
import math
from .baseDriver import *

class NaverCrawler(BaseDriver):
    baseUrl = 'https://section.blog.naver.com/BlogHome.nhn?directoryNo=0&currentPage=1&groupId=0'

    def run(self, keyword: str = ''):
        self.submit_keyword(
            selector='//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/input',
            keyword='LG ThinQ',
        )

        postNumTag = FindType.XPATH.get_element(
            self.driver,
            '//*[@id="content"]/section/div[1]/div[2]/span/span/em'
        )
        numbers = re.findall('[0-9]+', postNumTag.text)
        postTotalNum = int(''.join(numbers))

        postNumperPage = len(FindType.CSS.get_elements(
            self.driver,
            "#content > section > div.area_list_search > div.list_search_post"
        ))
        totalPage = math.ceil(postTotalNum/postNumperPage)

        pageUrlFormat = self.driver.current_url
        pageUrlFormat = pageUrlFormat.replace("pageNo=1", "pageNo={}")

        # TODO multu processing
        # workerNum = 5
        # workNum = math.ceil(totalPage/workerNum)
        # page_list = list(range(totalPage))
        # work_list = list(divide_chunks(page_list, workNum))

        for i in range(totalPage):
            pageUrl = pageUrlFormat.format(i+1)
            self.driver.get(pageUrl)
            posts = FindType.CSS.get_elements(
                self.driver,
                '#content > section > div.area_list_search > div.list_search_post > div > div.info_post > div.desc > a.desc_inner'
            )
            for p in posts:
                href = p.get_attribute('href')
                self.urls.append(href)
            break

        print(self.urls)



    def get_cotent(self, url):
        content = {}
        self.driver.get(url)


    def get_title(self):
        return FindType.CSS.get_element(self.driver, '#SE-283bdf3c-df3d-47de-aa9e-953e5df49448 > div > div > div.pcol1 > div')










