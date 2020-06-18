from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from flask_mail import Mail
from werkzeug import secure_filename
from datetime import datetime
import json
import os
import logging
import sys
import math

with open('config.json', 'r') as c:
    params = json.load(c)['params']

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

app.secret_key = 'this-really-needs-to-be-changed'

# app.config['SESSION_TYPE'] = 'filesystem'

# sess.init_app(app)
# app.config['UPLOAD_FOLDER'] = params['upload_location']
# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME=params['gmail-user'],
#     MAIL_PASSWORD=params['gmail-password']
# )
# mail = Mail(app)

if params['local_server']:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://bcowlfcvbfungl:3397db728933b1336930480c1d4b998b0b893625524a771f9772aa80dcea7d71@ec2-52-87-135-240.compute-1.amazonaws.com:5432/d76ut71fodb9or"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://bcowlfcvbfungl:3397db728933b1336930480c1d4b998b0b893625524a771f9772aa80dcea7d71@ec2-52-87-135-240.compute-1.amazonaws.com:5432/d76ut71fodb9or"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Contacts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    mob_num = db.Column(db.String(12), unique=True, nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

    def __repr__(self):
        return f'<Contact {self.name}>'
    
class Posts(db.Model):
    
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    tagline = db.Column(db.String(500), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)


@app.route('/')
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_posts']))
    # print(f'type last: {type(last)}')
    # [0:params['no_of_posts']]
    page = request.args.get('page')
    # print(f'page: {page}, type: {type(page)}')
    if not str(page).isnumeric():
        page = 1
        
    page = int(page)
    # print(f'page type: {type(page)}')
    # print(f'params[no of posts] type: {type(params["no_of_posts"])}')
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
            # print(f'sno: {sno}')
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
        # mail.send_message('New message from: ' + name,
        #                   sender=email, recipients=[params['gmail-user']],
        #                   body=message + "\n" + phone)
    return render_template('contact.html', params=params)


@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    # fetch post from db
    post = Posts.query.filter_by(slug=post_slug).first()
    # print(post)
    return render_template('post.html', params=params, post=post)


if __name__ == "__main__":
    app.run()
