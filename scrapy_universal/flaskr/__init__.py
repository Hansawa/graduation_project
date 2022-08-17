import os
import pathlib

from flask import Flask


def create_app(test_config=None):
    # flaskr 路径
    flaskrPath = os.path.join(os.getcwd(), __name__.split('.')[1])
    # create and configure the app, 添加了 instance_relative_config 为 True 后配置文件存放在 instance 目录里
    app = Flask(__name__, instance_relative_config=True, instance_path=os.path.join(flaskrPath, 'instance'))
    app.config.from_mapping(
        SECRET_KEY='dev2',
        SQLITE_DB=os.path.join(app.instance_path, 'flaskr.sqlite'),
        MONGODB_URI='localhost',
        CRAWLER_CONFIGS_DIR=os.path.join(flaskrPath, 'crawler_configs')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    pathlib.Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(app.config['CRAWLER_CONFIGS_DIR']).mkdir(parents=True, exist_ok=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 注册数据库
    from scrapy_universal.flaskr.DBHelper import sqlitedb
    sqlitedb.init_app(app)

    from scrapy_universal.flaskr.DBHelper import mongodb
    mongodb.init_app(app)

    # 注册蓝图
    from .blueprints import crawler
    app.register_blueprint(crawler.bp)

    return app
