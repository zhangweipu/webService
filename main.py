from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

app.template_folder = 'pages'


@app.route("/hello")
def print_hi():
    return render_template('index.html')


@app.route("/str")
def get_str():
    return '{"name":"aaa"}'


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
