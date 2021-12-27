from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forumdata.sqlite"
db = SQLAlchemy(app)
@app.route('/businessregister', methods = ['POST'])
def businessregister():
    Businessname = request.form["Businessname"]
    businesstypeID = request.form["BusinesstypeID"] #no idea how to get this, please fix this line
    Userid = request.form["Userid"]#no idea how to get this, please fix this line
    searchdata = sqlite3.connect("forumdata.sqlite")
    newbusiness = [(Businessname, businesstypeID, Userid)]
    sqlInsert = """INSERT INTO business(name, business_type_id, user_id) VALUES(?, ?, ?)"""
    cursor1 = searchdata.cursor()
    cursor1.executemany(sqlInsert, newbusiness) #Add the business to the database.
    searchdata.close()
    return render_template('/login.html') #return the login page