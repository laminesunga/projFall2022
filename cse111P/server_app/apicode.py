
os.chdir(r'C:\Users\lamin\OneDrive\Documents\CSE-106\Flack_envir\env\Lib\site-packages')
app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.sqlite"

db = SQLAlchemy(app)
class Classes(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String, unique=True, nullable=False)
    c_departid = db.Column(db.INTEGER, nullable= False)
    c_capacity = db.Column(db.INTEGER, nullable=False)
    c_enrollNumber =db.Column(db.INTEGER, nullable = False)
    c_description = db.Column(db.String, nullable= False)
    c_days = db.Column(db.String, nullable=False)
    c_start_time = db.Column(db.String, nullable=False) 
    c_end_time = db.Column(db.String, nullable=False)
    Instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False) 
    Instructor = db.relationship('Instructor', backref=db.backref('instructor', lazy=True))
    

class Instructor(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    i_name = db.Column(db.String, nullable=False) 
    User_Id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    Users = db.relationship('Users', backref=db.backref('users', lazy=False)) 

class Users(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    Username = db.Column(db.String, unique=True, nullable=False) 
    Password = db.Column(db.String, nullable=False)

class Students(db.Model):
    id= db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String, unique=True, nullable=False)
    s_phone = db.Column(db.String,unique = True, nullable=False)
    s_birthdate = db.Column(db.String, nullable=False)
    User_Id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
     
    
class Enrollment(db.Model):

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    e_grade = db.Column(db.INTEGER, nullable=False)
    e_courseid = db.Column(db.INTEGER, db.ForeignKey('classes.id'), nullable=False) 
    Classes = db.relationship('Classes', backref=db.backref('classes', lazy=True))
    e_studentid = db.Column(db.INTEGER, db.ForeignKey('students.id'), nullable=False) 
    Students = db.relationship('Students', backref=db.backref('students', lazy=True))
    

admin = Admin(app, name="ABC University", template_mode='bootstrap3')
admin.add_view(ModelView(Users,db.session))
admin.add_view(ModelView(Students,db.session))
admin.add_view(ModelView(Instructor,db.session))
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
        sqlTeacher = """ SELECT DISTINCT users.Username, Password
                        FROM users, instructor
                        WHERE users.Username = instructor.User_Id """
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
                return redirect(url_for('teacherview', username = User)) #go to the teacher view with that teacher name
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

    tempSn = request.args.get('User_Id')
    studsearch = Students.query.filter_by(User_Id=tempSn).first()
    sId= studsearch.id

    sName = studsearch.s_name

    if request.method == 'POST':
            cId = request.form['cid']
            print("class id in backend is " + str(cId))
            
            check = bool (Enrollment.query.filter_by(e_studentid=sId,e_courseid = cId).first())
            print(check)
            if check :
                print(check)
                rem = Enrollment.query.filter_by(e_studentid=sId,e_courseid = cId).first()
                db.session.delete(rem)
                c = Classes.query.filter_by(id=cId).first()
                c.c_enrollNumber -= 1
                db.session.commit()
                print("committed!")

            else:           ## Add an entry in enrollment table
                student = Enrollment(e_courseid=cId, e_studentid=sId,e_grade=0)
                db.session.add(student)
                c = Classes.query.filter_by(id=cId).first()
                c.c_enrollNumber += 1
                db.session.commit()
                print("committed!")

    return render_template( 'student.html', uid= tempSn, nm=sName, tempSid = sId, 
                            classes = Classes.query.all(),
                            enrollment= Enrollment.query.filter_by(e_studentid=sId).all() )

@app.route('/teacherview/<username>')
def teacherview(username):
    #find the that professor via User_Id and rediret it to the /<name> page
    searchdata = sqlite3.connect("school.sqlite")
    sqlFindTeacher = """SELECT i_name
                        FROM instructor
                        WHERE User_id = ?"""
    arg = [username]
    cursor1 = searchdata.cursor()
    cursor1.execute(sqlFindTeacher, arg)
    rows1 = cursor1.fetchall()
    list2 = []
    for k in rows1:
        s = "{}".format(*k)
        list2.append(s)

    

    sqlFindallclasse = """ SELECT c_name,i_name,c_capacity,c_enrollNumber,c_start_time,c_end_time
                                   From instructor,classes
                                   Where classes.Instructor_Id = instructor.id
                                         and instructor.User_Id = ?"""
    arg = [username]
    cursor2 = searchdata.cursor()
    cursor2.execute(sqlFindallclasse, arg)
    res = cursor2.fetchall()

    # os.chdir(r'C:\Users\lamin\OneDrive\Documents\CSE-106\Flack_envir\env\Lib\site-packages')
    # with open("out.txt","w") as file:
    List = []
    word = []
    
    fdata = []
    
    
    for k in res:
        s = "{} {} {} {} {} {}".format(*k)
        List.append(s)
    print (List)
    for k in List:
        a = [k.split()]
        word.extend(a)
    for k in word:
        list1 = []
        cn = k[0] + " " + k[1]
        pn = k[2] + " " + k[3]
        c = k[4] 
        e =  k[5]
        st =  k[6]+ " "+k[7]
        et =k[8]+" "+k[9]
    
        list1.append(cn)
        list1.append(pn)
        list1.append(c)
        list1.append(e)
        list1.append(st)
        list1.append(et)



        print(list1)
        fdata.append(list1)

    print(fdata)
                
    
    searchdata.close()
    return render_template('teacherview.html', data = fdata, value = list2, username = username)
   # return 'Hello Dr. %s!' % rows1[0] #change this line!


@app.route('/gradeview/<username>/<c_name>/', methods = ['POST','GET'])
def gradeview(username,c_name):
    searchdata = sqlite3.connect("school.sqlite")
    sqlFindgrade = """ SELECT s_name,e_grade
                                   From instructor,classes,students,enrollment
                                   Where classes.Instructor_Id = instructor.id and
                                   c_name = ? and 
                                   instructor.User_id = ?  and
                                   classes.id = e_courseid and
                                   e_studentid = students.id """

    arg = [c_name,username]
    cursor3 = searchdata.cursor()
    cursor3.execute(sqlFindgrade, arg)
    res = cursor3.fetchall()
    print (c_name)
    print (res)
  
    fdata =[]
    for k in res:
        name = k[0]
        grade = k[1]
        fdata.append([name,grade])
    

    sql4=""" select min(e_grade), max(e_grade),AVG(e_grade)
             From enrollment,instructor, classes,students
                Where classes.Instructor_Id = instructor.id and
                        c_name = ? and 
                        instructor.User_id = ? and
                        classes.id = e_courseid ;"""
    arg = [c_name,username]
    
    cu12 = searchdata.cursor()
    cu12.execute(sql4,arg)
    resi= cu12.fetchall()

    print ("this is fdata")
    print(fdata)
    if request.method == 'POST':
        
        g = request.form['grd']
        print(g)
       
        sql = """ Update enrollment
                      Set e_grade = e_grade + ?
                      Where e_studentid   IN (select students.id 
                                     From students, enrollment,classes,instructor
                                     where students.id = enrollment.e_studentid and
                                     enrollment.e_courseid = classes.id and
                                     classes.Instructor_Id = instructor.id and
                                     instructor.User_Id = ? and
                                     classes.c_name= ? )"""
        searchdata.cursor()
        searchdata.execute(sql,(g,username,c_name))
        searchdata.commit()
        searchdata.close()
        return redirect(url_for('gradeview',username=username,c_name=c_name))
    
    else:
     searchdata.close()
     return render_template('gradeview.html', data1= fdata,username = username,c_name = c_name,ave=resi )

@app.route('/gradeview/<username>/<c_name>/<s_name>/', methods = ['POST','GET'])
def editgrade(username,c_name,s_name):
 print(username)
 print(c_name)
 print(s_name)

 if request.method == 'POST':
    
    new_grade = request.form['grade']
    print(new_grade)
    searchdata = sqlite3.connect("school.sqlite")
    sqledit = """ UPDATE enrollment
                  SET e_grade = ? 
                  WHERE e_studentid IN (Select students.id 
                  From enrollment,students,classes
                  Where students.id = e_studentid and
                  s_name = ? and
                  e_courseid = classes.id and
                  c_name = ?) """
    
    arg = [new_grade,s_name,c_name]
    searchdata.execute(sqledit, arg)
    searchdata.commit()
    searchdata.close()
    print(1)


    return redirect(url_for('gradeview',username=username,c_name=c_name))
 else:
    return render_template('editgrade.html',username=username,c_name=c_name,s_name=s_name)



@app.route('/admin')
def index():
    return render_template('index.html')

@app.route('/admin/newstudent/', methods =['POST','GET'])
def newstudent():
    searchdata = sqlite3.connect("school.sqlite")

    sql = """ select s_name,User_id
                      from students """
    cur=searchdata.cursor()
    cur.execute(sql)
    res = cur.fetchall()

    if  request.method =='POST':
        
        
        funct=request.form['status']
        
        if funct =="add":
            
            print(funct)
            

            sn = request.form['name']
            sun = request.form['usern']
            sp = request.form['phone']
            bd = request.form['birthdate']
            
            print(sn)
            print(sun)
            print(sp)
            print(bd)

            
            sql=(""" insert into students (s_name,User_Id,s_phone,s_birthdate)
                        Values(?,?,?,?)""")
            sql2=(""" insert into users (Username,Password)
                    Values (?,?)""")
            searchdata.execute(sql,(sn,sun,sp,bd,))
            searchdata.commit()
            searchdata.execute(sql2,(sun,sun))
            searchdata.commit()
            success = "record added"

            print('student added to record')

            return redirect(url_for('newstudent'))

    
        if funct == "info":
            argm= request.form['sid']
            
            sql = """ select c_name,c_description,e_grade,c_days,i_name
                      from students,users,classes,enrollment,instructor
                      where users.Username= ? and
                      students.User_Id = users.Username and
                      students.Id = enrollment.e_studentid and
                      enrollment.e_courseid = classes.id and
                      classes.Instructor_Id = instructor.Id """
            
            cur=searchdata.cursor()
            cur.execute(sql,(argm,))
            res1=cur.fetchall()
            
            return render_template('newstudent.html',allst=res,info = res1)
    else:
        return render_template('newstudent.html',allst=res)

    


@app.route('/admin/newinstruc/', methods =['POST','GET'])
def newinstruc():
    searchdata = sqlite3.connect("school.sqlite")

    sql = """ select i_name,User_id
            from instructor """
    cur=searchdata.cursor()
    cur.execute(sql)
    resall = cur.fetchall()

    if  request.method =='POST':

        funct=request.form['status']

        if funct =="add":

            sn = request.form['name']
            sun = request.form['usern']
        
            print(sn)
            print(sun)
            
            sql=(""" insert into instructor (i_name,User_Id)
                        Values(?,?)""")
            sql2=(""" insert into users (Username,Password)
                    Values (?,?)""")
            searchdata.execute(sql,(sn,sun,))
            searchdata.commit()
            searchdata.execute(sql2,(sun,sun))
            searchdata.commit()

            print('instructor added to record adde to record')

            return redirect(url_for('newinstruc'))
       

        if funct == "info" :
            argm= request.form['sid']
          
            sql2= """select i_name,c_name,d_name,c_description
                     from instructor, Departement, classes,users,Planning
                     where users.Username = ?  and
                     instructor.User_Id = users.Username and
                     instructor.id = classes.Instructor_Id and
                     instructor.id=planning.p_instrid
                     group by c_name; """

            cur=searchdata.cursor()
            cur.execute(sql2,(argm,))
            res1 = cur.fetchall()
            return(render_template('newinstruc.html',onei=res1,allinst=resall))
            


    else:
        return render_template('newinstruc.html',allinst=resall)

@app.route('/admin/newclasse/', methods =['POST','GET'])
def newclasse():
    searchdata = sqlite3.connect("school.sqlite")
    if  request.method =='POST':
        cn = request.form['name']
        iid = request.form['instid']
        did = request.form['departid']
        ca = request.form['capa']
        ce = request.form['enrol']
        des = request.form['desc']
        d = request.form['days']
        s = request.form['start']
        e = request.form['end']
        

        
        sql=(""" insert into classes (c_name,Instructor_Id,c_departid,c_capacity,c_enrollNumber,c_description,c_days,c_start_time,c_end_time)
                    Values(?,?,?,?,?,?,?,?,?)""")

        searchdata.execute(sql,(cn,iid,did,ca,ce,des,d,s,e))
        searchdata.commit()


        print('instructor added to record adde to record')

        return redirect(url_for('index'))
    else:
        return render_template('newclasse.html')

if __name__ == '__main__':
     app.run()
     
