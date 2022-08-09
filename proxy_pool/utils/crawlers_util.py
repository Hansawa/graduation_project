"""dynamically, get all the crawler classes from the package 'crawlers' without giving any class name.

"""
import os
import pkgutil
import importlib
import inspect
import sys
import time

import psutil

import proxy_pool.crawlers as crawlers_pkg
from proxy_pool.crawlers.base_crawler import BaseCrawler


class CrawlersUtil:
    """

    """
    @staticmethod
    def get_crawlers_cls():
        """

        :return:
        """
        crawlers_cls = []
        for module_info in pkgutil.walk_packages(crawlers_pkg.__path__, f'{crawlers_pkg.__name__}.'):
            if not module_info.ispkg:
                module = importlib.import_module(module_info.name)
                for name, value in inspect.getmembers(module):
                    if inspect.isclass(value) and issubclass(value, BaseCrawler) and value is not BaseCrawler \
                            and not getattr(value, 'ignore', False):
                        crawlers_cls.append(value)
        return crawlers_cls


if __name__ == '__main__':
    for i in range(5):
        print(CrawlersUtil.get_crawlers_cls())
        time.sleep(2)

