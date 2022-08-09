# 读取配置文件，将内容转成 json 对象并返回
from os.path import realpath, dirname, join
import json


# __file__：执行该文件时所使用的路径，可能是相对路径或绝对路径
# realpath：获取一个路径（文件）的绝对路径或真实路径（而不是软链接的路径）
# dirname：返回路径中的目录部分
# 在 python 中，"/" 与 "\" 都可以作为路径分隔符，但在普通字符串中 "\" 被作为转义字符头，因此需要使用转义字符 "\\"
# 在 linux 中路径分隔符为斜杠 "/"
# encoding='utf8' 意思为使用 utf-8 的编码方式来读取文件
# read()：逐个字节或字符（由 mode 确定）读取文件并将内容以字符串的形式返回
# json.loads()：将字符串转换成 python 对象，如字典，列表，基本类型等。在此为转换成字典
# os.path.join() 会将每一个字符串用路径分隔符连接起来
def get_config(name):
    path = join(dirname(realpath(__file__)), 'configs', f'{name}.json')
    with open(path, 'r', encoding='utf8') as f:
        return json.loads(f.read())
