"""

"""
import asyncio
import selectors
import time
import aiohttp
from proxy_pool.storages.redis_client import RedisClient


class Tester:
    """

    """
    def __init__(self):
        self.redis_client = RedisClient()

    async def test_pertask(self, session, proxy):
        try:
            # 测试匿名性
            # url = 'https://www.httpbin.org/ip'
            # async with session.get(url) as resp:
            #     resp_ip = await resp.json()
            #     origin_ip = resp_ip['origin']
            #     print(origin_ip)
            # async with session.get(url, proxy=f'http://{proxy}') as resp:
            #     json_ip = await resp.json()
            #     proxy_ip = json_ip['origin']
            #     print(proxy, proxy_ip)
            #     assert origin_ip != proxy_ip
            #     assert proxy == proxy_ip
            url = 'http://www.baidu.com'
            async with session.get(url, proxy=f'http://{proxy}', allow_redirects=False) as resp:
                if resp.status == 200:
                    self.redis_client.maximize_score(proxy)
                    print(resp.status)
                else:
                    self.redis_client.decrease_score(proxy)
        except Exception as e:
            self.redis_client.decrease_score(proxy)
            print(f'Error: {e}')

    async def test_tasks(self, proxies):
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [asyncio.create_task(self.test_pertask(session, proxy)) for proxy in proxies]
            await asyncio.gather(*tasks)

    def run(self):
        start = time.time()

        cursor = 0
        # 获取事件循环来存放并执行异步任务
        selector = selectors.SelectSelector()
        loop = asyncio.SelectorEventLoop(selector)
        while True:
            cursor, proxies = self.redis_client.get_batch(cursor=cursor, count=50)
            loop.run_until_complete(self.test_tasks(proxies))
            # 如果使用如下语句的话，事件循环会二次关闭，导致异常
            # asyncio.run(self.test_tasks())
            if not cursor:
                loop.close()
                print(f'event loop is closed: {loop.is_closed()}')
                break

        end = time.time()
        print(f'cost time: {end - start}')


if __name__ == '__main__':
    for _ in range(1):
        Tester().run()
