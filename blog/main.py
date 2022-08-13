from flask import Flask, render_template, request, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import json

app = Flask(__name__)
app.secret_key = 'super-secret-key'

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

@app.route('/dashboard', methods=["GET", "POST"])
def login():
    if "user" in session and session['user'] == params['username']:
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)
    
    if request.method == "POST":
        # Redirect to admin panel
        data = request.form.to_dict()
        username = data['uname']
        userpass = data['upass']
        # print(data)
        if username == params['username'] and userpass == params['password']:
            # set the session variable
            session['user'] = username
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)
        
    else :
        return render_template('/login.html', params=params)


@app.route("/edit/<string:sno>", methods=["GET", "POST"])
def edit(sno):
    if 'user' in session and session['user']==params['username']:
        
        if request.method=='POST':
            data = request.form.to_dict()
            title = data['title']
            # tline = data['tline']
            slug = data['slug']
            content = data['content']
            img_file = data['img_file']
            date = datetime.now()

        ## FACING ERROR
        # if sno=='0':
        #     post = Posts(title=title, slug=slug, content=content, img_file=img_file, date=date)
        #     db.session.add(post)
        #     db.session.commit()
        
        # else:
        #     post = Posts.query.filter_by(sno=sno).first()
        #     post.box_title = title
        #     # post.tline = tline
        #     post.slug = slug
        #     post.content = content
        #     post.img_file = img_file
        #     post.date = date
        #     db.session.commit()
        #     return redirect('/edit/'+sno)
        

    post = Posts.query.filter_by(sno=sno).first()
    return render_template('/edit.html', params=params, post=post)
    

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