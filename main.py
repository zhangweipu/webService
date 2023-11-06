from flask import Flask, request, render_template

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8083)
