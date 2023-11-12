import logging

from flask import Flask, request, render_template, abort, jsonify
import subprocess

from network.BaseResponse import BaseResponse
from network.BaseRequest import BaseRequest
from security import encodeUtil

from entity import Person

app = Flask(__name__)

app.template_folder = 'pages'


@app.before_request
def intercept():
    custom_header_value = request.headers.get('author')
    logging.debug(custom_header_value)
    if custom_header_value is None:
        response = BaseResponse(403, "error", "error")
        abort(jsonify(response))
    encrypt = encodeUtil.aes_encrypt(custom_header_value)
    logging.debug('密钥：'+encrypt)
    if custom_header_value != "test":
        response = BaseResponse(403, "error", "error")
        abort(jsonify(response))


@app.route("/hello")
def print_hi():
    return render_template('index.html')


@app.route("/str")
def get_str():
    s = encodeUtil.aes_encrypt("aaa", "xxxx")
    stra = 'ssss'
    stra.ljust(32, '\0')[:32]
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
