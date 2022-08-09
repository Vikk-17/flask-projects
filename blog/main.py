from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)


with open("config.json", mode='r') as c:
    params = json.load(c)["params"]

local_server = True
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)


@app.route('/')
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_post']]
    return render_template('/index.html', params=params, posts=posts)


@app.route('/about')
def about():
    return render_template('/about.html', params=params)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        """Fetch data and add it to the database"""
        data = request.form.to_dict()
        name = data['name']
        phone = data['number']
        message = data['message']
        email = data['email']
        #print(data)
        
        entry = Contacts(name=name, email=email, phone_num=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('/contact.html', params=params)

@app.route('/post/<string:post_slug>', methods=["GET"])
def post_route(post_slug):
    # Fetch data from database
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('/post.html', params=params, post=post)