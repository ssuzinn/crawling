import os
import re
import math
import json
from settings import cur_path, KST
from crawler.BaseDriver import *


class NaverCrawler(BaseDriver):
    baseurl = 'https://section.blog.naver.com/BlogHome.nhn?directoryNo=0&currentPage=1&groupId=0'
    url_file_path = os.path.join(cur_path, '건강관리_urls.json')
    #content_file_path = os.path.join(cur_path, 'contents.json')
    base_content_css_path = "#printPost1 > tbody > tr > td.bcc > div.wrap_rabbit"
    content_css_path = ""
    E = []

    def run(self, keyword: str):
        if os.path.isfile(self.url_file_path):
            with open(self.url_file_path, 'r') as urlf:
                self.url_list = json.load(urlf)
        else:
            self.save_links(keyword=keyword)


        for link in self.url_list:
            try:
                self.get_content(link=link)
            except:
                self.E.append(link)

        self.content_file_path = os.path.join(cur_path, f'contents_{keyword}.json')
        with open(self.content_file_path, 'w',encoding='utf8') as cf:
            json.dump(self.contents, cf, indent="\t", ensure_ascii=False)

        if len(self.E) != 1:
            with open(f'error_links_{keyword}.json', mode='w') as urlEf:
                json.dump(self.E, urlEf, indent="\t", ensure_ascii=False)

    def save_links(self, keyword: str):
        self.submit_keyword(
            selector='//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/input',
            keyword=keyword
        )

        content_num = FindType.XPATH.get_element(driver=self.driver,
                                                 selector='//*[@id="content"]/section/div[1]/div[2]/span/span/em')
        numbers = re.findall('[0-9]+', content_num.text)
        post_total_num = int(''.join(numbers))

        url = self.driver.current_url
        page_url_format = url.replace("pageNo=1", 'pageNo={}')

        page_content_num = len(
            FindType.CSS.get_elements(
                driver=self.driver,
                selector='#content > section > div.area_list_search >div.list_search_post'
            )
        )

        total_page = math.ceil(post_total_num / page_content_num)
        print(total_page)
        for p in range(total_page):
            self.driver.get(page_url_format.format(p + 1))
            posts = FindType.CSS.get_elements(
                driver=self.driver,
                selector='#content > section > div.area_list_search > div.list_search_post > div > div.info_post > div.desc > a.desc_inner'
            )
            if len(posts) != 1:
                for post in posts:
                    href = post.get_attribute('href')
                    self.url_list.append(href)
            else:
                last_url = posts[0].get_attribute('href')
                if last_url in self.url_list:
                    break

        with open(self.url_file_path, mode='wt') as urlf:
            json.dump(self.url_list, urlf, indent="\t", ensure_ascii=False)

    def get_content(self, link):
        self.driver.get(link)
        self.driver.switch_to.frame('mainFrame')
        self.content_css_path = f'{self.base_content_css_path}'
        self.get_title()
        self.get_body()
        self.save_content(link=link)
        self.driver.switch_to.default_content()

    def get_title(self):
        try:
            title_element = FindType.CSS.get_element(
                driver=self.driver,
                selector=f'{self.content_css_path} > div.se-viewer > div.se-documentTitle > div.se-component-content > div.se-section-documentTitle'
            )
        except:
            self.content_css_path = f"{self.content_css_path} > div.view"
            title_element = FindType.CSS.get_element(
                driver=self.driver,
                selector=f'{self.content_css_path} > div.se-viewer > div.se-documentTitle > div.se-component-content > div.se-section-documentTitle'
            )

        # series
        # div > div.blog2_series

        self.title = title_element.find_element_by_css_selector("div.pcol1").text
        print(self.title)
        _time = title_element.find_element_by_css_selector("div.blog2_container > span.se_publishDate")
        self.publish_date = datetime.strptime(_time.text, "%Y. %m. %d. %H:%M").astimezone(tz=KST)
        print(self.publish_date)

        # soup = BeautifulSoup(html, 'html.parser')
        # return soup.title.string

    def get_body(self):
        content_element = FindType.CSS.get_element(
            driver=self.driver,
            selector=f'{self.content_css_path} > div.se-viewer > div.se-main-container'
        )
        text_containers = content_element.find_elements_by_css_selector("div.se-text")
        text_list = [tc.text for tc in text_containers]
        self.body = "\n".join(text_list)

        print(self.body)

    def save_content(self, link):
        self.contents.append({
            "link": link,
            "title": self.title,
            "content": self.body,
            "publish_date": self.publish_date.strftime("%Y-%m-%d %H:%M:%S %Z")
        })
