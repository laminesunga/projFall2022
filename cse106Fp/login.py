from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forumdata.sqlite"
db = SQLAlchemy(app)
@app.route('/', methods = ['POST'])
def login():
    User = request.form["Username"]
    Password = request.form["Password"]
    searchdata = sqlite3.connect("forumdata.sqlite")
    sqlUser = """SELECT username, salted_pass, role_type_id
                 FROM users """ #search the database for the user
    cursor1 = searchdata.cursor()
    cursor1.execute(sqlUser) #access the User table
    rows1 = cursor1.fetchall()
    for r1 in rows1: #find whether that is a user in the forum
        if(User == r1[2] and Password == r1[3] and r1[4] == 1):
            return redirect(url_for('userview', User_Id = User)) #go to the user view of the forum
         if(User == r1[2] and Password == r1[3] and r1[4] == 2):
            return redirect(url_for('businessview', User_Id = User)) #go to the business view of the forum
         if(User == r1[2] and Password == r1[3] and r1[4] == 3):
            return redirect(url_for('adminview', User_Id = User)) #go to the admin view of the forum
        if(User == r1[2] and Password != r1[1]):  #add the case when the user enters wrong password but correct username
            return "Wrong Password! Try again!"
    searchdata.close()
    return 'The user does not exist! Please register!' #add the case when the username and password are not in the database. The user does not exist.
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
    sqlFindBusiness = """SELECT fullname
                        FROM users
                        WHERE users.username = ?"""
    arg = [User_Id]
    cursor1 = searchdata.cursor()
    cursor1.execute(sqlFindBusiness, arg)
    rows1 = cursor1.fetchall()
    return 'Hello %s!' % rows1[0] #change this line! It needs to display the forum

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