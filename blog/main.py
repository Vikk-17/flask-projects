from flask import Flask, render_template, request, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime
import json
import os
from werkzeug.utils import secure_filename
import math


app = Flask(__name__)
app.secret_key = 'super-secret-key'



with open("config.json", mode='r') as c:
    params = json.load(c)["params"]

app.config['UPLOAD_FOLDER'] = params['upload_location']

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
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_post']))
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_post']):(page-1)*int(params['no_of_post'])+ int(params['no_of_post'])]
    # posts = posts[(page-1)*int(params['no_of_post']):(page-1)*int(params['no_of_post'])+int(params['no_of_post'])]
    if page==1:
        prev = '#'
        next = '/?page=' + str(page+1)
    elif page==last:
        prev = '/?page=' + str(page-1)
        next = '#'
    else:
        prev = '/?page=' + str(page-1)
        next = '/?page=' + str(page+1)
    # posts = Posts.query.filter_by().all()[0:params['no_of_post']]
    return render_template('/index.html', params=params, posts=posts, prev=prev, next=next)


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
    

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if 'user' in session and session['user']==params['username']:
        
        if request.method=='POST':
            inp_file = request.files['file1']
            inp_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(inp_file.filename)))
            return "Uploaded successfully"


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route("/delete/<string:sno>" , methods=['GET', 'POST'])
def delete(sno):
    if "user" in session and session['user']==params['username']:
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect("/dashboard")

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