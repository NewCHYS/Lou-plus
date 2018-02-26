from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    dir1 = '/home/shiyanlou/files/'
    list1 = os.listdir(dir1)
    s = ''
    for name in list1:
        filepath = os.path.join(dir1, name)
        if os.path.isfile(filepath):
            with open(filepath) as f:
                load = json.load(f)
            s += load['title'] + '\n'
    return s

@app.route('/files/<filename>')
def file(filename):
    dir1 = '/home/shiyanlou/files/'
    filename += '.json'
    s = ''
    filepath = os.path.join(dir1, filename)
    if os.path.isfile(filepath):
        with open(filepath) as f:
            load = json.load(f)
        s = json.dumps(load)
    else:
        return render_template('404.html'), 404
    return s

@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()

