from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, Text
from flask_migrate import Migrate
from werkzeug import secure_filename
from datetime import datetime
import json
import os
import math

with open('info.json', 'r') as info:
    params = json.load(info)['params']

app = Flask(__name__)
app.secret_key = 'this-really-needs-to-be-changed'

database_url = os.getenv(
    'DATABASE_URL',
    default='postgresql://postgres:12345@localhost:5432/flask-blog-db',  # E.g., for local dev
)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

db = SQLAlchemy(app)
print(f'#### db.engine.url ###: {db.engine.url}')
migrate = Migrate(app, db)

class Contacts(db.Model):
    __tablename__ = 'contacts'

    sno = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(20), nullable=False)
    mob_num = Column(String(12), unique=True, nullable=False)
    msg = Column(String(120), nullable=False)
    date = Column(DateTime, nullable=True)

    def __init__(self, name, email, mob_num, msg, date):
        self.name = name
        self.email = email
        self.mob_num = mob_num
        self.msg = msg
        self.date = date

    def __repr__(self):
        return '<sno {}>'.format(self.sno)


class Posts(db.Model):
    __tablename__ = 'posts'

    sno = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    tagline = Column(String(500), nullable=False)
    slug = Column(String(30), nullable=False)
    content = Column(Text, nullable=False)
    date = Column(DateTime, nullable=True)
    img_file = Column(String(12), nullable=True)

    def __init__(self, title, tagline, slug, content, date, img_file):
        self.title = title
        self.tagline = tagline
        self.slug = slug
        self.content = content
        self.date = date
        self.img_file = img_file

    def __repr__(self):
        return '<sno {}>'.format(self.sno)


"""
heroku run python
>>> from app import db
>>> db.create_all()
>>> db.session.commit()
"""


# if not params['local_server']:
db.create_all()
db.session.commit()
# app.logger.info('Tables have been created!')


@app.route('/')
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_posts']))
    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1

    page = int(page)
    posts = posts[(page - 1) * int(params['no_of_posts']): (page - 1) * int(params['no_of_posts']) + int(
        params['no_of_posts'])]

    if page == 1:
        prev = "#"
        next = '/?page=' + str(page + 1)

    elif page == last:
        next = "#"
        prev = '/?page=' + str(page - 1)
    else:
        prev = '/?page=' + str(page - 1)
        next = '/?page=' + str(page + 1)

    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/edit/<string:sno>', methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            title = request.form.get('title')
            tagline = request.form.get('tagline')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            date = datetime.now()
            print(f'current date: {date}')
            # base64.b64decode(date)
            print(f'after base64: current date: {date}')
            if sno == '0':
                post = Posts(title=title, slug=slug, content=content, img_file=img_file, tagline=tagline, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = title
                post.slug = slug
                post.content = content
                post.tagline = tagline
                post.img_file = img_file
                post.date = date
                print(f'current date: {date}')
                db.session.commit()
                return redirect('/edit/' + sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post, sno=sno)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_user']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)
    if request.method == 'POST':
        # redirect to admin panel
        username = request.form.get('uname')
        password = request.form.get('pass')
        if username == params['admin_user'] and password == params['admin_password']:
            # set the session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)

    return render_template('login.html', params=params)


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded successfully!!"


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route('/delete/<string:sno>', methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # add entry to db
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, mob_num=phone, email=email, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)


@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    # fetch post from db
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


if __name__ == "__main__":
    app.run()
