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


class KakaoReviewCrawler:
    def __init__(self):
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_argument('headless')
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

        # 검색된 정보가 있는 경우에만 탐색
        # 1번 페이지 place list 읽기
        html = self.driver.page_source

        soup = BeautifulSoup(html, 'html.parser')
        place_lists = soup.select('.placelist > .PlaceItem')  # 검색된 장소 목록

        # 검색된 첫 페이지 장소 목록 크롤링하기
        self.crawling(place, place_lists)
        search_area.clear()

        # 우선 더보기 클릭해서 2페이지
        try:
            self.driver.find_element(By.XPATH, '//*[@id="info.search.place.more"]').send_keys(Keys.ENTER)
            sleep(1)

            # 2~ 5페이지 읽기
            for i in range(2, 6):
                # 페이지 넘기기
                xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
                self.driver.find_element(By.XPATH, xPath).send_keys(Keys.ENTER)
                sleep(1)

                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                place_lists = soup.select('.placelist > .PlaceItem')  # 장소 목록 list

                self.crawling(place, place_lists)

        except ElementNotInteractableException:
            print('not found')
        finally:
            search_area.clear()

    def crawling(self, place, place_lists):
        """
        페이지 목록을 받아서 크롤링 하는 함수
        :param place: 리뷰 정보 찾을 장소이름
        """

        while_flag = False
        for i, place in enumerate(place_lists):
            # 광고에 따라서 index 조정해야함
            # if i >= 3:
            #   i += 1

            place_name = place.select('.head_item > .tit_name > .link_name')[0].text  # place name
            place_address = place.select('.info_item > .addr > p')[0].text  # place address

            detail_page_xpath = '//*[@id="info.search.place.list"]/li[' + str(i + 1) + ']/div[5]/div[4]/a[1]'
            self.driver.find_element(By.XPATH, detail_page_xpath).send_keys(Keys.ENTER)
            self.driver.switch_to.window(self.driver.window_handles[-1])  # 상세정보 탭으로 변환
            sleep(1)

            # 첫 페이지
            self.extract_review(place_name)

            # 2-5 페이지
            idx = 3
            try:
                page_num = len(self.driver.find_elements(By.CLASS_NAME, 'link_page'))  # 페이지 수 찾기
                for i in range(page_num - 1):
                    # css selector를 이용해 페이지 버튼 누르기
                    self.driver.find_element(By.CSS_SELECTOR,
                                             '#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(
                                                 idx) + ')').send_keys(Keys.ENTER)
                    sleep(1)
                    self.extract_review(place_name)
                    idx += 1
                self.driver.find_element(By.LINK_TEXT, "다음").send_keys(Keys.ENTER)  # 5페이지가 넘는 경우 다음 버튼 누르기
                sleep(1)
                self.extract_review(place_name)  # 리뷰 추출
            except (NoSuchElementException, ElementNotInteractableException):
                print("no review in crawling")

            # 그 이후 페이지
            while True:
                idx = 4
                try:
                    page_num = len(self.driver.find_elements(By.CLASS_NAME, 'link_page'))
                    for i in range(page_num - 1):
                        self.driver.find_element(By.CSS_SELECTOR,
                                                 '#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child(' + str(
                                                     idx) + ')').send_keys(Keys.ENTER)
                        sleep(1)
                        self.extract_review(place_name)
                        idx += 1
                    self.driver.find_element(By.LINK_TEXT, '다음').send_keys(Keys.ENTER)  # 10페이지 이상으로 넘어가기 위한 다음 버튼 클릭
                    sleep(1)
                    self.extract_review(place_name)  # 리뷰 추출
                except (NoSuchElementException, ElementNotInteractableException):
                    print("no review in crawling")
                    break

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])  # 검색 탭으로 전환

    def extract_review(self, place_name):
        ret = True

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 첫 페이지 리뷰 목록 찾기
        review_lists = soup.select('.list_evaluation > li')

        # 리뷰가 있는 경우
        if len(review_lists) != 0:
            for i, review in enumerate(review_lists):
                comment = review.select('.txt_comment > span')  # 리뷰
                rating = review.select('.grade_star > em')  # 별점
                val = ''
                if len(comment) != 0:
                    if len(rating) != 0:
                        val = comment[0].text + '-' + rating[0].text  # .replace('점', '')
                    else:
                        val = comment[0].text + '/0'
                    print(val)

        else:
            # print('no review in extract')
            ret = False

        return ret
