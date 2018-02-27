from flask import Flask, render_template, abort
import os
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.setdefault('SQLACHEMY_TRACK_MODIFICATIONS', True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/userdata'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', backref=db.backref('file', lazy='dynamic'))

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name

@app.route('/')
def index():
    files = File.query.all()
    print(files)
    title = ''
    s = ''
    for title in files:
        print(title.title)
        print(type(title.title))
        s += '<a href="/files/' + str(title.id) + '">' + title.title + '</a></p>'
    return s

@app.route('/files/<file_id>')
def file(file_id):
    try:
        files = File.query.filter_by(id=file_id).first()
        s = ''
        s += 'Category: ' + files.category.name + '</p>'
        s += 'Content: ' + files.content + '</p>'
        s += 'Created Time: ' + datetime.strftime(files.created_time, '%Y-%m-%d %H:%M:%S') + '</p>'
        return s
    except:
        return render_template('404.html'), 404

@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


'''
db.create_all()
java = Category('Java')
python = Category('Python')
file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
db.session.add(java)
db.session.add(python)
db.session.add(file1)
db.session.add(file2)
db.session.commit()
'''

if __name__ == '__main__':
    app.run()

