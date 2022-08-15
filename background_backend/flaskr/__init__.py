import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLITE_DB=os.path.join(app.instance_path, 'flaskr.sqlite'),
        MONGODB_URI='localhost',
        MONGODB_DB='bgbe',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 注册数据库
    from . import sqlitedb
    sqlitedb.init_app(app)

    from . import mongodb
    mongodb.init_app(app)

    # 注册蓝图
    from . import admin
    app.register_blueprint(admin.bp)

    return app
