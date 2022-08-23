# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo


# 我们可以自己定义 pipeline，而且必须实现 process_item() 方法，最后要在 settings.py 中注册该 pipeline
class MongoPipeline:
    # 初始化方法（相当于构造方法）
    def __init__(self, mongo_uri, mongo_db, collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection = collection
        self.client = None
        self.db = None

    """
        方法类别: 类方法
        可实现的位置: 每一个 spider、pipeline 或 middlewares 都可以存在该类方法
        如何执行: 只要在项目全局配置文件中注册当前类就可以被 scrapy 框架检测到并执行
        作用: 类似于依赖注入（item pipeline 依赖于当前类）。
            实例化当前类并返回注入到 item pipeline 中，且实例化时传入的参数值可以从项目全局配置文件中获取。
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            collection=crawler.settings.get('COLLECTION')
        )

    # 当爬虫打开后，连接 mongodb
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri)
        # 获取数据库
        self.db = self.client[self.mongo_db]

    # 必须要实现的方法
    # 当 engine 将一个 item 传入 pipelines 且到达当前 pipeline 时执行此方法进行数据清洗、验证或存储等工作
    def process_item(self, item, spider):
        # 获取 collection 并插入数据
        # pymongo 4.0 之后的版本中剔除了 Collection.insert() 方法，改成了 insert_one(字典) 与 insert_many(字典列表)
        # 使用 update_one 避免插入重复数据，此处接受三个参数，filter: 要更改的元素，update: 更改后的元素的值，upsert: 启用更新与插入功能
        # item['title'] = item.fields.get('title')
        self.db[self.collection].update_one({'title': item['title']}, {'$set': item}, upsert=True)
        return item

    # 当爬虫关闭后，关闭 mongodb
    def close_spider(self, spider):
        self.client.close()
