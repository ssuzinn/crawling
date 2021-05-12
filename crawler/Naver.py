import re
import math
from crawler.BaseDriver import *
import urllib.request
from bs4 import BeautifulSoup
import time

class NaverCrawler(BaseDriver):
    baseurl='https://section.blog.naver.com/BlogHome.nhn?directoryNo=0&currentPage=1&groupId=0'
    def run (self,keyword:str):
        self.submit_keyword(
            selector='//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/input',
            keyword=keyword
        )


        content_num=FindType.XPATH.get_element(driver=self.driver,
                                 selector='//*[@id="content"]/section/div[1]/div[2]/span/span/em')
        numbers=re.findall('[0-9]+', content_num.text)
        postTotalnum=int(''.join(numbers))


        url=self.driver.current_url
        pageurlformat=url.replace("pageNo=1",'pageNo={}')

        pagecontentnum=len(FindType.CSS.get_elements(driver=self.driver,
                                  selector='#content > section > div.area_list_search >div.list_search_post'))
        total_page=math.ceil(postTotalnum/pagecontentnum)
        urls=[]
        for p in range(total_page):
           self.driver.get(pageurlformat.format(p+1))
           posts=FindType.CSS.get_elements(
               driver=self.driver,
               selector='#content > section > div.area_list_search > div.list_search_post > div > div.info_post > div.desc > a.desc_inner'
           )
           if len(posts) != 1:
               for post in posts:
                   href=post.get_attribute('href')
                   urls.append(href)

           if len(posts) == 1:
               urls.append(posts[0].get_attribute('href'))
               break


        f=open('urllist.txt', mode='wt')
        for url in urls:
            f.write(url +'\n')
        f.close()


class NaverBlog(BaseDriver):
    f=open('./urllist.txt')
    urls=[t.strip() for t in f.readlines()]
    baseurl =urls[0]
    def run(self,keyword=None):
        pass
    def get_title(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup.title.string
    def get_content(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.get_text())
        content = soup.find_all(class_='se-text-paragraph se-text-paragraph-align-center ')

        return content












