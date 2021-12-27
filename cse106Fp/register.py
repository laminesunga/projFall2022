from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forumdata.sqlite"
db = SQLAlchemy(app)
@app.route('/register', methods = ['POST'])
def register():
    Fullname = request.form["Fullname"]
    User = request.form["Username"]
    Password = request.form["Password"]
    roleid = request.form["roleid"]
    searchdata = sqlite3.connect("forumdata.sqlite")
    newuser = [(Fullname, User, Password, roleid)]
    sqlInsert = """INSERT INTO users(fullname, username, salted pass, role_type_id) VALUES(?, ?, ?, ?)"""
    cursor1 = searchdata.cursor()
    cursor1.execute(sqlInsert, newuser) #Add the user to the database.
    searchdata.close()
    if (roleid == 1 or roleid == 3):
        return render_template('/login.html') #If it is a user or admin return to the login page
    if (roleid == 2):
        return render_template('/businessregister.html') #go the register page for business to fill the business and business_type table
    
    