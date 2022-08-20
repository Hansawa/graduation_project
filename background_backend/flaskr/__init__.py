import os
import pathlib

from flask import Flask


# 工厂函数
def create_app(test_config=None):
    # flask 实例名
    flaskr_path = os.path.join(os.getcwd(), __name__.split('.')[1])
    # create and configure the app, 添加了 instance_relative_config 为 True 后配置文件存放在 instance 目录里
    app = Flask(__name__, instance_relative_config=True, instance_path=os.path.join(flaskr_path, 'instance'))
    app.config.from_mapping(
        SECRET_KEY='dev1',
        SQLITE_DB=os.path.join(app.instance_path, 'flaskr.sqlite'),
        MONGODB_URI='localhost',
        CRAWLER_CONFIGS_DIR=os.path.join(flaskr_path, 'crawler_configs'),
        CRAWLER_TEST_CONFIGS_DIR=os.path.join(flaskr_path, 'crawler_configs', 'test')
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
    pathlib.Path(app.config['CRAWLER_TEST_CONFIGS_DIR']).mkdir(parents=True, exist_ok=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 注册数据库
    from background_backend.flaskr.DBHelper import sqlitedb
    sqlitedb.init_app(app)

    from background_backend.flaskr.DBHelper import mongodb
    mongodb.init_app(app)

    # 注册蓝图
    from .blueprints.admin import admin
    app.register_blueprint(admin.bp)

    from .blueprints.admin import crawler
    app.register_blueprint(crawler.bp)

    from .blueprints.admin import raw_news
    app.register_blueprint(raw_news.bp)

    from .blueprints.admin import test_news
    app.register_blueprint(test_news.bp)

    # 跨域支持
    def after_request(resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    app.after_request(after_request)

    return app
