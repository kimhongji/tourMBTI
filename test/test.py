import kakaoReviewCrawler
import tourAPI
from storage.redis import RedisConn

redisCon = RedisConn()

if __name__ == "__main__":
    # tourAPI 를 통해 관광지 리스트 추출
    api = tourAPI.TourAPI(tourAPI.AreaCodes.SEOUL)
    contentTypeIds = [12]
    tourList = []
    for tour in api.get_tour_list(contentTypeIds):
        tourList.append(tour['title'])

    # 각 관광지에 대한 카카오 맵 리뷰 크롤링
    crawler = kakaoReviewCrawler.KakaoReviewCrawler()
    for place_name in tourList:
        if not redisCon.is_place_review_exist(place_name):
            print("=======", place_name, "=======")
            crawler.search(place_name)
            print("=======", "end", "=======")

    del api
    del crawler
