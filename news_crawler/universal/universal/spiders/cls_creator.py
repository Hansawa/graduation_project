from scrapy import Field, Item
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Compose, Join
import re


# 动态生成 UniversalItem 类
def get_cls_universal_item(attrs):
    ui_attrs = {}
    for key in attrs.keys():
        ui_attrs[f'{key}'] = Field()
    UniversalItem = type('UniversalItem', (Item,), ui_attrs)
    return UniversalItem


# 动态生成 UniversalLoader 类
def get_cls_universal_loader(default_processor, attrs):
    # default_processor
    ul_attrs = {}
    for key, processors in default_processor.items():
        string = ''
        for processor in processors:
            # 检查安全
            if 'import' in processor.lower() or 'module' in processor.lower():
                raise ValueError
            string = string + f'{processor},'
        # 去掉末尾“，”
        string = string[0: len(string) - 1]
        # 设置 loader 的 default_processor，in or out
        ul_attrs[f'default_{key}put_processor'] = eval(f'Compose({string})')
    # item processor： item_name：属性名，value：属性对应的处理程序，key：in out，processors：处理器
    for item_name, value in attrs.items():
        for key, processors in value.get('processor').items():
            string = ''
            for processor in processors:
                # 检查安全
                if 'import' in processor.lower() or 'module' in processor.lower():
                    raise ValueError
                string = string + f'{processor},'
            string = string[0: len(string) - 1]
            ul_attrs[f'{item_name}_{key}'] = eval(f'Compose({string})')
    UniversalLoader = type('UniversalLoader', (ItemLoader,), ul_attrs)
    return UniversalLoader
