#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, current_app, request, url_for, Response, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin, login_user, logout_user, login_required
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


app = Flask(__name__)
app.config.update(
    SECRET_KEY='SeriouslydevelopedbyJailman',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
)


db = SQLAlchemy(app)
# db.init_app(app)
# #define egine
# engine = db.create_engine('sqlite:///test.db')
# #bind metadata
# metadata = db.MetaData(engine)
# metadata.create_all(engine)
# #get db connected
# conn = engine.connect()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    fullname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    

    def __init__(self, id, name, fullname, email, password_hash):
        self.id = id
        self.name = name
        self.fullname = fullname
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return "%d/%s/%s/%s/%s" % (self.id, self.name, self.fullname, self.email, self.password_hash)



@login_manager.user_loader
def load_user(id, name, fullname, email, password_hash):
    return User(id, name, fullname, email, password_hash)


db.create_all()
admin = User(1, 'jack', 'jack wong', 'jailman@sina.com', '111')
# db.session.add(admin)
db.session.commit()
# users = User.query.all()
# print users



#参考
# class BlogPost(db.Model):

#     __tablename__ = "posts"

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     description = db.Column(db.String, nullable=False)

#     def __init__(self, title, description):
#         self.title = title
#         self.description = description

#     def __repr__(self):
#         return '<title {}'.format(self.title)


# from app import db
# from models import BlogPost

# # create the database and the db table
# db.create_all()

# # insert data
# db.session.add(BlogPost("Good", "I\'m good."))
# db.session.add(BlogPost("Well", "I\'m well."))
# db.session.add(BlogPost("Excellent", "I\'m excellent."))
# db.session.add(BlogPost("Okay", "I\'m okay."))

# # commit the changes
# db.session.commit()



# some protected url
@app.route('/')
@login_required
def home():
    return Response("Hello World!")

 
# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == '111' and username == 'jack':
            login_user(admin)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')



if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 80,
        debug = True
    )