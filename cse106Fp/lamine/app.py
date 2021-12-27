from enum import unique
import re
import os
from sqlite3 import Error
from os import name
from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask.helpers import url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView, view
from flask_admin import Admin
from sqlalchemy.orm import query
from werkzeug.utils import redirect
from flask_login import LoginManager,current_user,login_user,login_required,logout_user
os.chdir(r'C:\Users\lamin\OneDrive\Documents\CSE-106\Flack_envir\env\Lib\site-packages')
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forumdata.sqlite"
db = SQLAlchemy(app)

class Business (db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    business_type_id = db.Column(db.INTEGER, nullable=False)
    user_id = db.Column(db.INTEGER, nullable=False)
    # Posts = db.relationship ('Posts', backref= db.backref('posts',lazy=True))
class Business_type(db.Model):
    id = db.Column(db.INTEGER, primary_key = True, autoincrement= True)
    type_name = db.Column(db.String, unique=True, nullable=False)
class Posts(db.Model):
    id = db.Column(db.INTEGER, primary_key = True, autoincrement= True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.INTEGER, nullable=False)
    created_date = db.Column(db.String, nullable=False)
    likes = db.Column(db.INTEGER, nullable = False)
    dislikes = db.Column(db.INTEGER, nullable = False)
class Replies(db.Model):
    id = db.Column(db.INTEGER, primary_key = True, autoincrement= True)
    message = db.Column(db.String, unique=True, nullable=False)
    post_id = db.Column(db.INTEGER, nullable = False)
    user_id= db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable = False)
    created_date = db.Column(db.String, nullable=False)
    likes = db.Column(db.INTEGER, nullable = False)
    dislikes = db.Column(db.INTEGER, nullable = False)
    Users = db.relationship('Users', backref=db.backref('users', lazy=True))

class Role_type(db.Model):
    id = db.Column(db.INTEGER, primary_key = True, autoincrement= True)
    name = db.Column(db.String, unique=True, nullable=False)
class Users(db.Model):
    id = db.Column(db.INTEGER, primary_key = True, autoincrement= True)
    fullname = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    salted_pass = db.Column(db.String, unique=True, nullable=False)
    # role_type_id = db.Column(db.INTEGER, db.Foreignkey('role_type.id'), nullable = False)



    
    


@app.route('/', methods = ['POST','GET'])
def login():
 if request.method == 'POST':
    User = request.form["Username"]
    Password = request.form["Password"]
    searchdata = sqlite3.connect("forumdata.sqlite")
    sqlUser = """SELECT username, salted_pass, role_type_id
                 FROM users """ #search the database for the user
    cursor1 = searchdata.cursor()
    cursor1.execute(sqlUser) #access the User table
    rows1 = cursor1.fetchall()
    print(rows1)
    for r1 in rows1: #find whether that is a user in the forum
        if(User == r1[2] and Password == r1[3] and r1[4] == 1):
            return redirect(url_for('userview', User_Id = User)) #go to the user view of the forum
        if(User == r1[0] and Password == r1[1] and r1[2] == 2):
            return redirect(url_for('businessview', User_Id = User)) #go to the business view of the forum
        if(User == r1[2] and Password == r1[3] and r1[4] == 3):
            return redirect(url_for('adminview', User_Id = User)) #go to the admin view of the forum
        if(User == r1[2] and Password != r1[1]):  #add the case when the user enters wrong password but correct username
            return "Wrong Password! Try again!"
    searchdata.close()
    return 'The user does not exist! Please register!' #add the case when the username and password are not in the database. The user does not exist.
 else: 
        #print("I am in else!")
        return render_template( 'login.html')

@app.route('/userview/<User_Id>')
def userview(User_Id):
    #find the that student via User_Id and rediret it to the /<name> page 
    searchdata = sqlite3.connect("forumdata.sqlite")
    sqlFindUser = """SELECT fullname
                        FROM users
                        WHERE users.username = ?"""
    arg = [User_Id]
    cursor = searchdata.cursor()
    cursor.execute(sqlFindUser, arg)
    rows1 = cursor.fetchall()
    searchdata.close()
    return 'Hello %s!' % rows1[0] #change this line! It needs to display the forum

@app.route('/businessview/<User_Id>')
def businessview(User_Id):
    #find the that professor via User_Id and rediret it to the /<name> page
    searchdata = sqlite3.connect("forumdata.sqlite")
   
    business_username = Users.query.filter_by(username = User_Id).first()
    business_name = Business.query.filter_by(user_id=business_username.id).first()
    business_post = Posts.query.filter_by(user_id = business_username.id).first()
    business_id = business_post.id
    b_name= business_name.name
    
    
  

    return render_template('businessview.html',name=b_name,buss= business_name,User_Id=User_Id,
                                            bpost= Posts.query.filter_by(user_id = business_username.id),creply= Replies.query.filter_by(post_id = business_id))
@app.route('/businessview/<User_Id>/Addd/',methods=['POST','GET'])
def funct(User_Id):
     User_Id = User_Id
     if request.method =='POST':
        title = request.form['title']
        desc = request.form['desc']
        
        post= Posts(title=title,description=desc,user_id= User_Id,likes=0,dislikes=0)
        db.session.add(post)
        db.session.commit()
        redirect(url_for('businessview',User_Id=User_Id))
     else:
       return render_template('funct.html',User_Id=User_Id)

@app.route('/adminview/<User_Id>')
def adminview(User_Id):
    #find the that professor via User_Id and rediret it to the /<name> page
    searchdata = sqlite3.connect("forumdata.sqlite")
    sqlFindAdmin = """SELECT fullname
                        FROM users
                        WHERE users.username = ?"""
    arg = [User_Id]
    cursor1 = searchdata.cursor()
    cursor1.execute(sqlFindAdmin, arg)
    rows1 = cursor1.fetchall()
    return 'Hello %s!' % rows1[0] #change this line! It needs to display the forum
  
   
if __name__ == '__main__':
    app.run()