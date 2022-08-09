"""relevant operation about Redis

"""
import redis
import random


class RedisClient:
    """

    """
    def __init__(self):
        self.__db = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='', decode_responses=True)
        print(f'ping: {self.__db.ping()}')
        print(f'version: {redis.__version__}')

    def add(self, proxy):
        """

        :param proxy:
        :return:
        """
        if self.__db.zadd('PROXYPOOL_PROXIES', {proxy: 10}) != 1:
            print(f'{proxy} insertion failed')

    def get_random(self):
        """

        :return:
        """
        proxies = self.__db.zrangebyscore('PROXYPOOL_PROXIES', 100, 100)
        if len(proxies):
            return random.choice(proxies)
        proxies = self.__db.zrangebyscore('PROXYPOOL_PROXIES', 0, 100)
        if len(proxies):
            return random.choice(proxies)

    def get_all(self):
        proxies = self.__db.zrangebyscore('PROXYPOOL_PROXIES', 0, 100)
        return proxies

    def get_batch(self, cursor=0, count=10):
        """

        :param cursor:
        :param count:
        :return: cursor and list of proxy
        """
        cursor, proxies_scores = self.__db.zscan('PROXYPOOL_PROXIES', cursor=cursor, count=count)
        return cursor, [proxy_score[0] for proxy_score in proxies_scores]

    def maximize_score(self, proxy):
        self.__db.zadd('PROXYPOOL_PROXIES', {proxy: 100})

    def decrease_score(self, proxy):
        score = self.__db.zincrby('PROXYPOOL_PROXIES', -100, proxy)
        if score <= 0:
            self.__db.zrem('PROXYPOOL_PROXIES', proxy)

if __name__ == '__main__':
    redisClient = RedisClient()
    print(redisClient.decrease_score('61.190.160.199:9999'))
    # cursor = 0
    # while True:
    #     cursor, num = redisClient.get_batch_proxy(cursor=cursor)
    #     print(num)
    #     if cursor == 0:
    #         break
