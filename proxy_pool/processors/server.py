"""Flask web server app

"""
from flask import Flask
from proxy_pool.processors.scheduler import Scheduler
from proxy_pool.storages.redis_client import RedisClient

app = Flask(__name__)

scheduler = Scheduler()
redis_client = RedisClient()


@app.route('/')
def index():
    """

    :return:
    """
    return '<h2>Welcome to my proxy pool</h2>'


@app.route('/run/<process_name>')
def run_process(process_name):
    """

    :param process_name:
    :return:
    """
    return scheduler.run_process(process_name)


@app.route('/stop/<process_name>')
def stop_process(process_name):
    """

    :param process_name:
    :return:
    """
    return scheduler.stop_process(process_name)


@app.route('/get/random')
def get_random_proxy():
    """

    :return:
    """
    return f'<h2>Get random proxy</h2><br />{redis_client.get_random()}'


@app.route('/get/all')
def get_all_proxy():
    """

    :return:
    """
    proxies = redis_client.get_all()
    return f"<h2>Show all available proxies</h2><br/>{'<br/>'.join(proxies)}<br/>the " \
           f"total is {len(proxies)}"


if __name__ == '__main__':
    app.run(debug=True)
