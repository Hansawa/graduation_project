from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Compose, Join


class UniversalLoader(ItemLoader):
    default_output_processor = Compose(TakeFirst(), str.strip)
#
#
# class ChinaVoiceLoader(NewsLoader):
#     pass
# lambda 匿名函数
# strip()：移除字符头尾的指定字符，默认为空格或换行符
