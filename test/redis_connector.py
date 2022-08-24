import os
import redis
from tourAPI import TourAPI, AreaCodes
import wiki_crawler

PLACE_INFO_PREFIX = "PLACE_INFO:"
PLACE_REVIEW_PREFIX = "PLACE_REVIEW:"
PLACE_WIKI_PREFIX = "PLACE_WIKI:"


class RedisConn:
    def __init__(self):
        # local: "localhost", docker: "host.docker.internal", other: from env
        self.redis_host = os.environ.get("REDIS_HOST", "34.64.150.242")
        self.redis_port = os.environ.get("REDIS_PORT", 6379)
        self.redis_db = os.environ.get("REDIS_DB", 0)
        self.redis_password = os.environ.get("REDIS_PASSWORD", "tourapi")
        self.redis_client = redis.StrictRedis(host=self.redis_host, db=self.redis_db, password=self.redis_password)

    def __del__(self):
        print("RedisConn Close")

    # about info
    def is_place_info_exist(self, place):
        key = PLACE_INFO_PREFIX + place
        return self.redis_client.exists(key.encode('UTF-8'))

    def set_place_info(self, place, info):
        key = PLACE_INFO_PREFIX + place
        self.redis_client.set(key, info)

    def get_place_info(self, place):
        key = PLACE_INFO_PREFIX + place

        return self.redis_client.get(key.encode('UTF-8')).decode('UTF-8')

    # about review
    def is_place_review_exist(self, place):
        key = PLACE_REVIEW_PREFIX + place
        return self.redis_client.exists(key.encode('UTF-8'))

    def get_place_reviews(self, place):
        key = PLACE_REVIEW_PREFIX + place
        reviews = []
        for i in range(0, self.redis_client.llen(key)):
            reviews.append(self.redis_client.lindex(key, i).decode('UTF-8'))
        return reviews

    # about wiki
    def is_place_wiki_exist(self, place):
        key = PLACE_WIKI_PREFIX + place
        return self.redis_client.exists(key.encode('UTF-8'))

    def set_place_wiki(self, place, txt):
        key = PLACE_WIKI_PREFIX + place
        self.redis_client.set(key, txt)

    def get_place_wiki(self, place):
        key = PLACE_WIKI_PREFIX + place
        return self.redis_client.get(key.encode('UTF-8')).decode('UTF-8')


if __name__ == "__main__":
    api = TourAPI(AreaCodes.SEOUL)
    contentTypeIds = [12]
    # print(api.get_tour_list())

    wiki = wiki_crawler.WiKiCrawler()

    redis_conn = RedisConn()
    for tour in api.get_tour_list(contentTypeIds):
        try:
            # print(tour['title'])
            # if not redis_conn.is_place_info_exist(tour['title']):
            #     detail = api.get_detail_common(tour['content_id'])
            #
            #     redis_conn.set_place_info(tour['title'], detail['overview'])
            #     print(redis_conn.get_place_info(tour['title']))
            print(tour['title'])
            if not redis_conn.is_place_wiki_exist(tour['title']):
                if wiki.is_exist(tour['title']):
                    text = wiki.search(tour['title'])
                    redis_conn.set_place_wiki(tour['title'], text)
                print(redis_conn.get_place_info(tour['title']))

            print("-- 완료 --")
        except Exception:
            print(Exception)
            break
