import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

from storage.redis import RedisConn

redisCon = RedisConn()


class KakaoReviewCrawler:
    def __init__(self):
        chrome_opts = webdriver.ChromeOptions()
        #chrome_opts.add_argument('headless')
        chrome_opts.add_argument('lang=ko_KR')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
        self.driver.implicitly_wait(4)  # 렌더링 될때까지 기다린다 4초
        self.driver.get('https://map.kakao.com/')  # 주소 가져오기

    def __del__(self):
        self.driver.quit()

    def search(self, place):
        search_area = self.driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')  # 검색 창
        search_area.send_keys(place)  # 검색어 입력
        self.driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
        sleep(1)
        # 1번 페이지 place list 읽기
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        place_lists = soup.select('.placelist > .PlaceItem')
        # 검색된 첫 장소 크롤링
        if len(place_lists) > 0:
            first_place = place_lists[0]
            self.crawling(first_place)
        search_area.clear()

    def crawling(self, place):
        place_name = place.select('.head_item > .tit_name > .link_name')[0].text  # place name
        if not redisCon.is_place_review_exist(place_name):
            place_address = place.select('.info_item > .addr > p')[0].text  # place address
            detail_page_xpath = '//*[@id="info.search.place.list"]/li[1]/div[5]/div[4]/a[1]'
            try:
                self.driver.find_element(By.XPATH, detail_page_xpath).send_keys(Keys.ENTER)
                self.driver.switch_to.window(self.driver.window_handles[-1])  # 상세정보 탭으로 변환
                sleep(1)
                try:
                    # review_page_idx
                    idx = 1
                    while True:
                        page_num = len(self.driver.find_elements(By.CLASS_NAME, 'link_page'))  # 페이지 수 찾기
                        self.extract_review(place_name)
                        sleep(1)
                        for i in range(page_num - 1):
                            idx += 1
                            self.driver.find_element(By.XPATH,
                                                     "//div[@id='mArticle']/div[contains(@class, 'cont_evaluation')]"
                                                     "/div[@class='evaluation_review']/div/a[@data-page=" +
                                                     str(idx) + "]").send_keys(Keys.ENTER)
                            sleep(1)
                            self.extract_review(place_name)
                        self.driver.find_element(By.LINK_TEXT, "다음").send_keys(Keys.ENTER)  # 5페이지가 넘는 경우 다음 버튼 누르기
                except (NoSuchElementException, ElementNotInteractableException):
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])  # 검색 탭으로 전환
            except (NoSuchElementException, ElementNotInteractableException):
                print("no review in crawling")

    def extract_review(self, place_name):
        ret = True
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 첫 페이지 리뷰 목록 찾기
        review_lists = soup.select('.list_evaluation > li')
        # 리뷰가 있는 경우
        if len(review_lists) != 0:
            for i, review in enumerate(review_lists):
                comment = review.select('.txt_comment > span')
                if len(comment) != 0:
                    review = comment[0].text
                    print("{}: {}".format(place_name, review))
                    if review != "":
                        redisCon.set_place_review(place_name, review)
        else:
            ret = False
        return ret
