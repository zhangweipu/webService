import logging
import sys

from flask import Flask, request, render_template, abort, jsonify
import subprocess

from network.BaseResponse import BaseResponse
from network.BaseRequest import BaseRequest
from security import encodeUtil

from entity import Person

import logging
from logging.handlers import RotatingFileHandler

from security.encodeUtil import SecurityUtils

app = Flask(__name__)

# 配置日志记录
log_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=5)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
log_handler.setLevel(logging.DEBUG)

app.logger.addHandler(log_handler)
app.logger.setLevel(logging.DEBUG)
app.logger.info('App startup')

app = Flask(__name__)

app.template_folder = 'pages'


def handle_uncatched_error(exctype, value, traceback):
    app.logger.error(f"Exception: {exctype}, {value}")
    app.logger.error("Traceback", exc_info=(exctype, value, traceback))


sys.excepthook = handle_uncatched_error


@app.before_request
def intercept():
    custom_header_value = request.headers.get('author')
    app.logger.info("请求到了 : " + str(custom_header_value is None))
    if custom_header_value is None:
        app.logger.info("author 是空")
        response = BaseResponse(403, "error", "error")
        abort(jsonify(response.__dict__()))
    else:
        app.logger.info("author : " + str(custom_header_value))
    encrypt = SecurityUtils.decrypt(SecurityUtils.key, SecurityUtils.iv, custom_header_value)
    app.logger.info('密钥：' + encrypt)
    if encrypt != "com.wp.itime":
        app.logger.info("密钥不正确")
        response = BaseResponse(403, "error", "error")
        abort(jsonify(response.__dict__()))
    else:
        app.logger.info("密钥正确")


@app.route("/hello")
def print_hi():
    return render_template('index.html')


@app.route("/str")
def get_str():
    app.logger.info("请求信息")
    s = "tom"
    person = Person(name=s)
    return jsonify(BaseResponse(data=person).__dict__())


@app.route("/submit", methods=['POST'])
def save_test():
    text = request.form['json_text']
    print(text)
    name = text
    return render_template('index.html', name=name)


@app.route("/update", methods=['POST'])
def update_service():
    shell_name = "./update.sh"
    result = subprocess.run(shell_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return "重启了" + str(result.returncode)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8083)
