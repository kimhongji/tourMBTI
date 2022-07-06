import os
import redis


class RedisConn:

    def __init__(self):
        # local: "localhost", docker: "host.docker.internal", other: from env
        self.redis_host = os.environ.get("REDIS_HOST", "localhost")
        self.redis_port = os.environ.get("REDIS_PORT", 6379)
        self.redis_db = os.environ.get("REDIS_DB", 0)
        self.redis_client = redis.StrictRedis(host=self.redis_host, db=self.redis_db)

    def __del__(self):
        print("RedisConn Close")

    def is_key_exist(self, key):
        return self.redis_client.exists(key.encode('UTF-8'))

    def set_place_review(self, place, review):
        self.redis_client.lpush(place, review)

    def set_place_review_list(self, place, review_list):
        for review in review_list:
            self.redis_client.lpush(place, review)

    def get_place_reviews(self, place):
        reviews = []
        for i in range(0, self.redis_client.llen(place)):
            reviews.append(self.redis_client.lindex(place, i).decode('UTF-8'))
        return reviews
