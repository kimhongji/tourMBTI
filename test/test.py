import kakaoReviewCrawler
import tourAPI
from storage.redis import RedisConn

if __name__ == "__main__":
    # tourAPI 를 통해 관광지 리스트 추출
    api = tourAPI.TourAPI(tourAPI.AreaCodes.SEOUL)
    contentTypeIds = [12, 14, 39]
    tourList = []
    for tour in api.get_tour_list(contentTypeIds):
        tourList.append(tour['title'])

    # 각 관광지에 대한 카카오 맵 리뷰 크롤링
    crawler = kakaoReviewCrawler.KakaoReviewCrawler()
    for tour in tourList:
        print("=======", tour, "=======")
        crawler.search(tour)
        print("=======", "end", "=======")

    del api
    del crawler