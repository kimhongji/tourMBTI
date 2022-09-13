import pymysql
import json

from NLP import NLP
from redis_connector import RedisConn
from tourAPI import TourAPI, AreaCodes


class MysqlConn:
    def __init__(self):
        self.db = pymysql.connect(
            user='root',
            passwd='tourapi',
            host='34.64.154.192',
            db='tour',
            charset='utf8',
        )
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        print("MysqlConn Close")

    def insert(self, name, keywords):
        sql = "Insert INTO tour_keywords (name, keywords) VALUES (%s, %s)"

        self.cursor.execute(sql, (name, keywords))
        self.db.commit()

    def is_exist(self, name):
        sql = "Select count(*) from tour_keywords where name=%s"

        self.cursor.execute(sql, name)
        cnt = self.cursor.fetchone()

        if cnt[0] > 0:
            return True
        else:
            return False


if __name__ == "__main__":
    api = TourAPI(AreaCodes.SEOUL)
    contentTypeIds = ["12"]

    redis_conn = RedisConn()
    mysql_conn = MysqlConn()
    for tour in api.get_tour_list(contentTypeIds):
        raw = []

        # reviews
        try:
            reviews = redis_conn.get_place_reviews(tour["title"])
            for review in reviews:
                raw.append(review)
        except:
            print("there is no reviews")

        # info
        try:
            info = redis_conn.get_place_info(tour["title"])
            raw.append(info)
        except:
            print("there is no info")

        # wiki
        try:
            if redis_conn.is_place_wiki_exist(tour["title"]):
                wiki = redis_conn.get_place_wiki(tour["title"])
                raw.append(wiki)
        except:
            print("there is no wiki")

        print(tour['title'])

        if mysql_conn.is_exist(tour['title']):
            print("continue")
            continue

        nlp = NLP()
        keywords = nlp.run(raw)

        # print(keywords)

        keyword_json = json.dumps(keywords, ensure_ascii=False)
        print(keyword_json)
        mysql_conn.insert(tour['title'], keyword_json)
