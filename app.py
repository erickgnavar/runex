# coding: utf-8
import os
from uuid import uuid4

from flask import Flask, request, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['post'])
def upload():
    code_file = request.files['code']
    filename = uuid4().hex
    code_file.save(os.path.join(BASE_DIR, 'code', filename))
    command_template = 'docker run --rm -v $(pwd)/code:/app -w /app {image} {command}'
    params = {
        'image': 'python:2.7',
        'command': 'python {}'.format(filename)
    }
    result = os.popen(command_template.format(**params)).read()
    return render_template('home.html', result=result)

if __name__ == '__main__':
    app.run()
