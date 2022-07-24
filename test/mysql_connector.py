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

    def insert(self, name, keywords):
        sql = "Insert INTO tour_keywords (Name, Keywords) VALUES (%s, %s)"

        self.cursor.execute(sql, (name, keywords))
        self.db.commit()



if __name__ == "__main__":
    api = TourAPI(AreaCodes.SEOUL)
    contentTypeIds = [12]

    redis_conn = RedisConn()
    mysql_conn = MysqlConn()
    for tour in api.get_tour_list(contentTypeIds):
        raw = []
        reviews = redis_conn.get_place_reviews(tour["title"])
        info = redis_conn.get_place_info(tour["title"])

        raw.append(reviews)
        raw.append(info)

        nlp = NLP()
        keywords = nlp.run(raw)

        print(keywords)

        keyword_json = json.dumps(keywords)
        mysql_conn.insert(tour['title'], keyword_json)






