from flask import Flask, render_template, url_for, request, redirect, Response
import json
from main import feed_content
import os

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main_page.html")


@app.route('/content/<code>')
def work_program(code):
    for file in os.listdir('data\\'):
        if file[0:6] == code:
            path_file = os.path.join('data\\', file)
            data = feed_content(path_file)
    return Response(json.dumps(data), mimetype='application/json; charset=utf-8')


@app.route('/content', methods=['POST', 'GET'])
def work_program1():
    if request.method == "POST":
        code = request.form['number']
        return redirect(url_for('work_program', code=code))


if __name__ == "__main__":
    app.run(debug=False)
