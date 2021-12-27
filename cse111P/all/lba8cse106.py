import re
from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask.helpers import url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from sqlalchemy.orm import query
from werkzeug.utils import redirect
from flask_login import LoginManager,current_user,login_user,login_required,logout_user

app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.sqlite"

db = SQLAlchemy(app)
class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Course_name = db.Column(db.String, unique=True, nullable=False) 
    Number_enrolled = db.Column(db.Integer, unique=True, nullable=False)
    Capacity = db.Column(db.Integer, unique=True, nullable=False)
    Time = db.Column(db.String, unique=True, nullable=False) 
    Teacher_Id = db.Column(db.Integer,unique = True ,nullable=False) 
    # Teachers = db.relationship('Teachers', backref=db.backref('teachers', lazy=True))

class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, unique=True, nullable=False) 
    User_Id = db.Column(db.String, nullable=False) 
    # Users = db.relationship('Users', backref=db.backref('users', lazy=False)) 

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False) 
    password = db.Column(db.String, nullable=False)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False) 
    User_Id = db.Column(db.String, nullable=False) 
     
    
class Enrollment(db.Model):
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Grade = db.Column(db.Integer, nullable=False) 
    Class_Id = db.Column(db.Integer, nullable=False)  
    Student_Id = db.Column(db.Integer, nullable=False) 
    

admin = Admin(app, name="ABC University", template_mode='bootstrap3')
admin.add_view(ModelView(Users,db.session))
admin.add_view(ModelView(Students,db.session))
admin.add_view(ModelView(Teachers,db.session))
admin.add_view(ModelView(Classes,db.session))
admin.add_view(ModelView(Enrollment,db.session))



@app.route('/', methods = ['GET','POST'])
def login():
    #print("I am in login!")
    if request.method == 'POST':
        print("I am in post!")
        User = request.form["Username"]
        Password = request.form["Password"]
        searchdata = sqlite3.connect("school.sqlite")
        sqlStudent = """SELECT DISTINCT Username, Password
                        FROM users, students
                        WHERE users.Username = students.User_Id """
        sqlTeacher = """ SELECT DISTINCT Username, Password
                        FROM users, teachers
                        WHERE users.Username = teachers.User_Id """
        sqladmind = """ SELECT DISTINCT Username, Password
                        FROM users """
             
        cursor1 = searchdata.cursor()
        cursor1.execute(sqlStudent) #access the students table
        rows1 = cursor1.fetchall()

        for r1 in rows1: #find whether that user is a student
            if(User == r1[0] and Password == r1[1]):
                print("I am trying to go to student view!")
                return redirect(url_for('student', User_Id = User)) #go to the student view with that student name
            if(User == r1[0] and Password != r1[1]):  #add the case when the user enters wrong password but correct username
                return "Wrong Password! Try again!"

        cursor2 = searchdata.cursor()
        cursor2.execute(sqlTeacher) #access the teachers table
        rows2 = cursor2.fetchall()

        for r2 in rows2: #find whether that user is a teacher
            if(User == r2[0] and Password == r2[1]):
                return redirect(url_for('teacherview', User_Id = User)) #go to the teacher view with that teacher name
            if(User == r2[0] and Password != r2[1]):  #add the case when the user enters wrong password but correct username
                return "Wrong Password! Try again!"
       

        cursor3 = searchdata.cursor()
        cursor3.execute(sqladmind) #access user
        rows3 = cursor3.fetchall()

        for r3 in rows3: #find whether that user is a admin
            #print( "i am in admin pas")
           
            if(User == r3[0] and Password == r3[1]):
                print("I am trying to go to admind view!")
                return redirect(url_for('index')) #go to admin view
            if(User == r3[0] and Password != r3[1]):  #add the case when the user enters wrong password but correct username
                return "Wrong Password! Try again!"
        searchdata.close()

        return 'The user does not exist!' #add the case when the username and password are not in the database. The user does not exist.

    else: 
        #print("I am in else!")
        return render_template( 'login.html')

@app.route('/student', methods = ['GET','POST'])
def student():
    #print(request.args.get('User_Id'))
    #print("I am in student view!")
    tempSn = request.args.get('User_Id')
    studsearch = Students.query.filter_by(User_Id=tempSn).first()
    sId= studsearch.id
    sName = studsearch.name

    #print ("my requet method is ")
    #print (request.method)
    ###print("Student id =" + str(sId))
    if request.method == 'POST':
        cId = request.form['cid']
        print("class id in backend is " + str(cId))

        ### Add an entry in enrollment table
        student = Enrollment(Class_Id=cId, Student_Id=sId,grade=0)
        db.session.add(student)
        
        # Query to find class id, to increment number_enrolled
        c = Classes.query.filter_by(id=cId).first()
        c.Number_enrolled += 1
        db.session.commit()
        print("committed!")

    return render_template( 'student.html', uid= tempSn, nm=sName, tempSid = sId, 
                            classes = Classes.query.all(), 
                            enrollment= Enrollment.query.filter_by(Student_Id=sId).all() )

@app.route('/teacherview/<User_Id>')
def teacherview(User_Id):
    #find the that professor via User_Id and rediret it to the /<name> page
    searchdata = sqlite3.connect("school.sqlite")
    sqlFindTeacher = """SELECT Name
                        FROM teachers
                        WHERE teachers.User_Id = ?"""
    arg = [User_Id]
    cursor1 = searchdata.cursor()
    cursor1.execute(sqlFindTeacher, arg)
    rows1 = cursor1.fetchall()
    list2 = []
    for k in rows1:
        s = "{}".format(*k)
        list2.append(s)

    

    sqlFindallclasse = """ SELECT Course_name,teachers.Name,Time,Number_enrolled
                                   From teachers,classes
                                   Where classes.Teacher_Id = teachers.Id and teachers.User_Id = ?"""
    arg = [User_Id]
    cursor2 = searchdata.cursor()
    cursor2.execute(sqlFindallclasse, arg)
    res = cursor2.fetchall()

    # os.chdir(r'C:\Users\lamin\OneDrive\Documents\CSE-106\Flack_envir\env\Lib\site-packages')
    # with open("out.txt","w") as file:
    List = []
    word = []
    
    fdata = []
    
    
    for k in res:
        s = "{} {} {} {}\n".format(*k)
        List.append(s)
    print (List)
    for k in List:
        a = [k.split()]
        word.extend(a)
    for k in word:
        list1 = []
        cn = k[0] + " " + k[1]
        pn = k[2] + " " + k[3]
        ct = k[4] + " " + k[5] +  " " + k[6]
        c = k[7]
        list1.append(cn)
        list1.append(pn)
        list1.append(ct)
        list1.append(c)

        print(list1)
        fdata.append(list1)

    print(fdata)
                
    
    searchdata.close()
    return render_template('teacherview.html', data = fdata, value = list2, User_Id = User_Id)
   # return 'Hello Dr. %s!' % rows1[0] #change this line!


@app.route('/gradeview/<User_Id>/<Class_name>/')
def gradeview(User_Id,Class_name):
    searchdata = sqlite3.connect("school.sqlite")
    sqlFindgrade = """ SELECT students.Name,enrollment.Grade
                                   From teachers,classes,students,enrollment
                                   Where classes.Teacher_Id = teachers.Id and
                                   classes.Course_name = ? and 
                                   teachers.User_Id = ?  and
                                   classes.Id = enrollment.Class_Id and
                                   enrollment.Student_Id = students.Id """

    arg = [Class_name,User_Id]
    cursor3 = searchdata.cursor()
    cursor3.execute(sqlFindgrade, arg)
    res = cursor3.fetchall()
    print (Class_name)
    print (res)
  
    fdata =[]
    for k in res:
        name = k[0]
        grade = k[1]
        fdata.append([name,grade])
      

    print ("this is fdata")
    print(fdata)
                
    
    searchdata.close()
   
    
    return render_template('gradeview.html', data1= fdata,User_Id = User_Id,Class_name = Class_name )

@app.route('/gradeview/<User_Id>/<Class_name>/<sname>/', methods = ['POST','GET'])
def editgrade(User_Id,Class_name,sname):
 print(User_Id)
 print(Class_name)
 print(sname)

 if request.method == 'POST':
    
    new_grade = request.form['grade']
    print(new_grade)
    searchdata = sqlite3.connect("school.sqlite")
    sqledit = f""" UPDATE enrollment
                  SET Grade = ? 
                  WHERE enrollment.Student_Id IN (Select Student_Id 
                  From enrollment,students,classes
                  Where students.Id = enrollment.Student_Id and
                  students.Name = ? and
                  enrollment.Class_Id = classes.Id and
                  classes.Course_name = ?) """
    print(0)
    arg = [new_grade,sname,Class_name]
    searchdata.execute(sqledit, arg)
    print(00)
    searchdata.commit()
    print(000),
    searchdata.close()
    print(1)


    return redirect(url_for('gradeview',User_Id=User_Id,Class_name=Class_name))
 else:
    return render_template('editgrade.html',User_Id=User_Id,Class_name=Class_name,sname=sname)

# @app.route('/admin', methods = ['GET','POST'])
# def admin():
#     login_manager = LoginManager()
#     login_manager.init_app(app)
#     login_manager.login_view = 'login'
#     app.secret_key = 'keep it secret,keep it safe'
#     admin = Admin(app, name="ACME University", template_mode='bootstrap3')
#     admin.add_view(ModelView(Users,db.session))
#     admin.add_view(ModelView(Students,db.session))
#     admin.add_view(ModelView(Teachers,db.session))
#     admin.add_view(ModelView(Classes,db.session))
#     admin.add_view(ModelView(Enrollment,db.session))

#     @login_manager.user_loader
#     def load_user(user_id):
#         return Users.get_id(user_id)

@app.route('/admin')
def index():
    return render_template('index.html')

if __name__ == '__main__':
     app.run()
     
