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


@app.route('/')
def home():
    return render_template('/index.html', params=params)
# @app.route('/index')
# def index():
#     return render_template('/index.html')

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

@app.route('/post')
def post():
    return render_template('/post.html', params=params)