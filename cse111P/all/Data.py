from os import replace
import sqlite3
from sqlite3 import *
from typing import Match
import numpy as np
import time
from random import randint, randrange

session_type = ''
session_id = 0
session_name = ''

def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def createTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create tables")

    try:
        sql = """CREATE TABLE Student (
        s_studentid INTEGER NOT NULL,
        s_name VARCHAR(50) NOT NULL,
        s_phone VARCHAR(20) NOT NULL,
        s_birthdate DATE FORMAT 'yyyy-mm-dd',
        s_password VARCHAR(50) NOT NULL,
        s_level INTEGER NOT NULL)"""

        _conn.execute(sql)
        print("Created 'Student'")
    except Error as e:
        print(e)

    try:
        sql = """CREATE TABLE Instructor (
        i_instrid INTEGER NOT NULL,
        i_name VARCHAR(50) NOT NULL,
        i_comment VARCHAR(100),
        i_password VARCHAR(50) NOT NULL)"""

        _conn.execute(sql)
        print("Created 'Instructor'")
    except Error as e:
        print(e)

    try:
        sql = """CREATE TABLE Enrollment (
        e_studentid INTEGER NOT NULL,
        e_courseid INTEGER NOT NULL,
        e_grade FLOAT NOT NULL)"""

        _conn.execute(sql)
        print("Created 'Enrollment'")
    except Error as e:
        print(e)

    try:
        sql = """CREATE TABLE Classes (
        c_courseid INTEGER NOT NULL,
        c_name VARCHAR(50) NOT NULL,
        c_instrid INTEGER NOT NULL,
        c_departid INTEGER NOT NULL,
        c_description VARCHAR(100),
        c_days VARCHAR(50) NOT NULL,
        c_start_time TIME FORMAT 'HH:MM',
        c_end_time TIME FORMAT 'HH:MM')"""

        _conn.execute(sql)
        print("Created 'Classes'")
    except Error as e:
        print(e)

    try:
        sql = """CREATE TABLE Semester (
        se_id INTEGER NOT NULL,
        se_name VARCHAR(50) NOT NULL)"""

        _conn.execute(sql)
        print("Created 'Semester'")
    except Error as e:
        print(e)

    try:
        sql = """CREATE TABLE Term (
        t_cid INTEGER NOT NULL,
        t_seid INTEGER NOT NULL)"""

        _conn.execute(sql)
        print("Created 'Term'")
    except Error as e:
        print(e)

    try:
        sql = """CREATE TABLE Departement (
        d_departid INTEGER NOT NULL,
        d_name INTEGER NOT NULL)"""

        _conn.execute(sql)
        print("Created 'Departement'")
    except Error as e:
        print(e)
    
    try:
        sql = """CREATE TABLE Planning (
        p_departid INTEGER NOT NULL,
        p_instrid INTEGER NOT NULL,
        p_comment VARCHAR (50) )"""

        _conn.execute(sql)
        print("Created 'Planning'")
    except Error as e:
        print(e)


    print("++++++++++++++++++++++++++++++++++")

def populateTable(conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate table")

    #-------------------------------------------------------------------------------
    print("populate student")

    f = open('students_names.txt', "r")

    id = 1000
    i = 1

    for line in f:

        phone = [str(randint(1, 9)),str(randint(0, 9)),str(randint(0, 9)),'-',
        str(randint(0, 9)),str(randint(0, 9)),str(randint(0, 9)),'-',
        str(randint(0, 9)),str(randint(0, 9)),str(randint(0, 9)),str(randint(0, 9))]

        num = ''

        for j in range(len(phone)):
            num += phone[j]

        birthday = ""

        year = randint(1999, 2004)

        month = randint(1,12)

        if month < 10:
            month = "0" + str(month)
        else:
            month = str(month)

        day = randint(1,30)

        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        birth_day = [str(year),'-',month,
        '-',day]

        for j in range(len(birth_day)):
            birthday += birth_day[j]
    
        level = 0

        if(year == 1999):

            level = 4

        elif(year == 2001):

            x = randint(1,2)

            if(x == 1):
                level = 3
            if(x == 2):
                level = 4

        elif(year == 2002):

            x = randint(1,2)

            if(x == 1):
                level = 2
            if(x == 2):
                level = 3

        elif(year == 2003):
            
            x = randint(1,2)

            if(x == 1):
                level = 1
            if(x == 2):
                level = 2

        else:
            level = 1

        password = "" 
        
        for j in range(randrange(8,15)):

            x = 0

            while(True):
                x = randrange(33,122)

                if(x == 34 or (x >= 36 and x <=47) or (x >= 58 and x <= 63) or (x >= 91 and x <= 96)):
                    continue
                    
                break

            password += chr(x)
            
        sql = f"""INSERT INTO Student
            (s_studentid, s_name, s_phone, s_birthdate, s_password, s_level)
            VALUES
            (?, ?, ?, ?, ?, ?)"""
        conn.execute(sql, [id + i, str(line[0:len(line)-1]), str(num), str(birthday),str(password), level])
        print(f"{id + i}, {str(line[0:3]) + '-' + str(line[4:5]) + '-' + str(line[6:7])}, {str(num)}, {str(birthday)}, {str(password)}, {level}")
        i += 1

    f.close()

    #-------------------------------------------------------------------------------
    
    print("populate Instructor")

    f = open('instructor_names.txt', "r")

    class_type = ['MATH', 'PHYS', 'CSE', 'PSYCH', 'WRI', 'SPANISH', 'ENGLISH', 
    'JAPANESE', 'ENGR', 'COGS', 'HIST', 'ART', 'CHEM', 'BIO']
    id = 9000
    k = 1

    course_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    course_instr = [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    
    course_des = [['Pre-Calculus', 'Calculus', 'Discrete Math', 'Linear Algebra', 'Optimization', 'ODEs/PDEs', 'Statistics'],
    ['Intro to Physics', 'Optics', 'Chaotic Systems', 'Phsyics Group Study', 'Intermediate Physics', 'Nuclear Physics', 'Quantum Physics'],
    ['Intro to CSE', 'Data Structures', 'Computer Organization', 'Algorithims', 'Computer Architecture', 'Machine Learning', 'Intro to Data Bases'],
    ['Intro to Psychology', 'Intermediate Human Psychology', 'Child Development', 'Criminal Psychology', 'Family/House Functions', 'Psychology Group Study', 'Advanced Psychology Theory'],
    ['Intro to Essay Writing', 'Classic Literature', 'Post-Modern Era Writing', 'Court House Writing', 'Current World Issues', 'Writing in Discipline', 'Professional Writing Seminar'],
    ['Spanish 001','Spanish 010','Spanish 020','Spanish 030','Spanish 110','Spanish 120','Spanish 132'],
    ['English 001','English 010','English 020','English 030','English 110','English 120','English 132'],
    ['Japanese 001','Japanese 010','Japanese 020','Japanese 030','Japanese 110','Japanese 120','Japanese 132'],
    ['Intro to Engineeing','Protyping Methods','Material Science','Structural Integrity Analysis','Therodynamics','Enginerring Professional Seminar','CAD based Designing'],
    ['Intro to Cog Sci', 'Intro to Lang and Linguistics', 'Cog Sci Research Methods', 'Modeling Social Behavior', 'Neuroscience with ML Application', 'Cog Sci and Emotions', 'Complex Adaptive Systems'],
    ['US History', 'Colonial Period', 'Silk Road', 'Policing and Race', 'History of Korea', 'Latin American Revolutions', 'Ancient Rome'],
    ['Intro to Media', 'Writing Love Songs', 'Music Studies', 'Theater and Cinema', 'Drawing 001', 'Drawing 005', 'Video 001'],
    ['Intro to Chem', 'General Chem 1', 'Organic Chem', 'Organic Synth and Mech', 'Biochemistry', 'Chem Thermo and Kinetics', 'Inorganic Chem'],
    ['Contemp. Bio', 'Molecular Bio', 'Biology Today', 'The Cell', 'Nutrition', 'Microbiology', 'Virology']]

    meets = [['Mon-Wed','7:30 AM','8:50 AM','10:30 AM','11:50 AM'],
    ['Tue-Thur','7:30 AM','8:50 AM','10:30 AM','11:50 AM'],
    ['Mon-Wed','7:30 AM','8:50 AM','12:00 PM', '1:20 PM'],
    ['Tue-Thur','9:00 AM','10:20 AM','9:00 PM', '10:20 PM'],
    ['Tue-Thur','6:00 PM','7:20 PM'],
    ['Mon-Wed','9:00 AM','10:20 AM','1:30 PM','2:50 PM'],
    ['Tue-Thur','1:30 PM','2:50 PM','4:30 PM','5:50 PM'],
    ['Tue-Thur','7:30 PM','8:50 PM'],
    ['Mon-Wed','9:00 PM', '10:20 PM'],
    ['Fri','7:30 AM','8:50 AM','9:00 AM','10:20 AM'],
    ['Fri','10:30 AM','11:50 AM','12:00 PM', '1:20 PM'],
    ['Fri','1:30 PM','2:50 PM','3:00 PM','4:20 PM'],
    ['Fri','4:30 PM','5:50 PM','6:00 PM','7:20 PM'],
    ['Fri','7:30 PM','8:50 PM','9:00 PM', '10:20 PM']]

    num_instructors = 0

    for line in f:

        num_instructors += 1

        comment = []

        while(True):

            i = 0
            lim = randrange(1,2)
            courses = []

            while i <= lim:

                x = randrange(0,14)

                if(course_count[x] < 7):
                    
                    new = True

                    for j in range(len(courses)):
                    
                        if x == courses[j]:
                            new = False
                            break

                    if(new == True):  

                        if(i < lim - 1):
                            comment.append(class_type[x])

                            course_count[x] += 1
                            courses.append(x)
                            course_instr[x].append(id + k)

                        else:
                            
                            comment.append(class_type[x])

                            course_count[x] += 1 
                            courses.append(x)
                            course_instr[x].append(id + k)
                    
                    else:

                        continue
                
                i += 1

            break

        password = "" 
        
        for j in range(randrange(8,15)):

            x = 0

            while(True):
                x = randrange(33,122)

                if(x == 34 or (x >= 36 and x <=47) or (x >= 58 and x <= 63) or (x >= 91 and x <= 96)):
                    continue
                    
                break

            password += chr(x)

        if(len(comment) == 0):
            sql = f"""     
            INSERT INTO Instructor
            VALUES (?,?,?,?)   """
            conn.execute(sql,[str(id + k),line[0:len(line)-1],'None', password])
            print(f"{id + k}|{line[0:len(line)-1]}|{'None'}|{password}\n")
        elif(len(comment) == 1):
            sql = f"""     
            INSERT INTO Instructor
            VALUES (?,?,?,?)   """
            conn.execute(sql,[str(id + k),line[0:len(line)-1],comment[0], password])
            print(f"{id + k}|{line[0:len(line)-1]}|{comment[0]}|{password}\n")
        elif(len(comment) == 2):
            sql = f"""     
            INSERT INTO Instructor
            VALUES (?,?,?,?)   """
            conn.execute(sql,[str(id + k),line[0:len(line)-1],f'{comment[0]},{comment[1]}', password])
            print(f"{id + k}|{line[0:len(line)-1]}|{comment[0]},{comment[1]}|{password}\n")
        
        k += 1

    f.close()               
    
    #----------------------------------------------------------------
    print("populate classes")

    base = 100

    for i in range(len(course_instr)):
        
        for j in range(len(course_instr[i])):

            course_name = str(class_type[i]) + str(100 + j)
            x = randrange(1,len(meets[i])-1)

            if(x % 2 == 0):
                x-= 1

            sql = f""" INSERT INTO Classes
                VALUES (?,?,?,?,?,?,?,?)"""
            conn.execute(sql,[((i + 1)* base) + j, course_name , course_instr[i][j], f"{(i + 1)*base}", course_des[i][j], meets[i][0], meets[i][x],meets[i][x + 1]])

    #-------------------------------------------------------------------------------
    print("populate enrollment")

    sql = """SELECT s_studentid
        FROM Student"""

    cursor = conn.cursor()
    cursor.execute(sql)
    student_ids = cursor.fetchall()

    sql = """SELECT c_courseid, c_days, c_start_time, c_end_time
        FROM Classes"""

    cursor.execute(sql)
    course_info = cursor.fetchall()

    for i in range(len(student_ids)):

        num_classes = randrange(3,5)
        class_ids = []
        
        j = 0
        while j < num_classes:
            course_index = randrange(1, len(course_info) - 1)

            id = course_info[course_index]

            if j == 0:
                class_ids.append(id)
                j += 1
                continue
            
            repeat = False

            for prev_id in class_ids:
                if(id[1] == prev_id[1] and id[2] == prev_id[2]):
                    repeat = True
                    break
            
            if repeat == True:
                continue        
            else:
                class_ids.append(id)
                j += 1

        for id in class_ids:
            sql = f"""     
                INSERT INTO Enrollment
                VALUES (?,?,?)   """

            conn.execute(sql,[int(student_ids[i][0]),int(id[0]),float(randrange(75,100))])
    
    #-------------------------------------------------------------------------------

    print("populate Departement")

    class_type = ['Mathematics', 'Physics', 'Computer Science', 'Psychology', 'Writing', 'Spanish', 'English', 
    'Japanese', 'Engineering', 'Cognitive Science', 'History', 'Arts', 'Chemistry', 'Biology']

    id = 100
    c = 1

    for sub in class_type:

        print(f"{id*c}|{sub}")

    
        sql = f"""     
                INSERT INTO Departement
                VALUES (?,?)   """
        conn.execute(sql,[str(id*c), sub])

        c += 1

    #----------------------------------------------------------------

    print("populate Planning")

    
    sql = f"""     
            INSERT INTO Planning
            VALUES (?,?,?)   """
    conn.execute(sql,['100','901','math'])

    sql = f"""     
            INSERT INTO Planning
            VALUES (?,?,?)   """
    conn.execute(sql,['100','902','math'])

    sql = f"""     
            INSERT INTO Planning
            VALUES (?,?,?)   """
    conn.execute(sql,['100','903','math'])

    sql = f"""     
            INSERT INTO Planning
            VALUES (?,?,?)   """
    conn.execute(sql,['200','901','phys'])

    sql = f"""     
            INSERT INTO Planning
            VALUES (?,?,?)   """
    conn.execute(sql,['200','903','phys'])

    sql = f"""     
            INSERT INTO Planning
            VALUES (?,?,?)   """
    conn.execute(sql,['300','902','chemi'])

    #----------------------------------------------------------------

    # sql = f"""
    #         INSERT INTO Semester
    #         VALUES (?,?)   """

    # for i in range(10):
    #     conn.execute(sql, [''])


def dropTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")
    

    try:
        sql = """DROP TABLE Departement"""

        _conn.execute(sql)
        
        print("Dropped 'Departement'")
    except Error as e:
        print(e)

    try:
        sql = """DROP TABLE Planning"""

        _conn.execute(sql)
        
        print("Dropped 'Planning'")
    except Error as e:
        print(e)

    try:
        sql = """DROP TABLE Student"""

        _conn.execute(sql)
        
        print("Dropped 'Student'")

    except Error as e:
        print(e)

    try:
        sql = """DROP TABLE Classes"""

        _conn.execute(sql)
        
        print("Dropped 'Classes'")
    except Error as e:
        print(e)

    try:
        sql = """DROP TABLE Enrollment"""

        _conn.execute(sql)
        
        print("Dropped 'Enrollment'")
    except Error as e:
        print(e)

    try:
        sql = """DROP TABLE Instructor"""

        _conn.execute(sql)
        
        print("Dropped 'Instructor'")
    except Error as e:
        print(e)

    try:
        sql = """DROP TABLE Semester"""

        _conn.execute(sql)
        
        print("Dropped 'Semester'")
    except Error as e:
        print(e)

    try:
        sql = """DROP TABLE Term"""

        _conn.execute(sql)
        
        print("Dropped 'Term'")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def login(conn):

    global session_type
    global session_id
    global session_name

    while(True):
        login_type = str(input('\nHello! Are you a student(s) or an instructor(i)? '))

        if(login_type == 's'):
            
            student_id = str(input('Please enter your student id: '))
            password = str(input('Please enter your password: '))

            sql = "SELECT s_studentid, s_password FROM Student"

            cursor = conn.cursor()
            cursor.execute(sql)
            keys = np.array(cursor.fetchall())

            key = [student_id, password]

            match = False

            for line in keys:
                if(key[0] == line[0]):
                    if(key[1] == line[1]):
                        match = True

                if(match == True):
                    break

            if(match == True):

                sql = "SELECT s_name FROM Student WHERE (s_studentid = " + str(student_id) + " )"
                cursor.execute(sql)
                name = cursor.fetchall()

                print(f'\nLogin Successful! Welcome {name[0][0]}!\n')
                session_type = 'Student' 
                session_id = student_id
                session_name = name[0][0]

                return
            
            else:
                print("Login Failed; Please make sure to enter a valid ID and password")

        elif(login_type == 'i'):

            instructor_id = str(input('Please enter your instructor id: '))
            password = str(input('Please enter your password: '))
            
            sql = "SELECT i_instrid, i_password FROM Instructor"

            cursor = conn.cursor()
            cursor.execute(sql)
            keys = np.array(cursor.fetchall())

            key = [instructor_id, password]

            match = False

            for line in keys:
                # print(f"key: {key} line: {line}")
                if(key[0] == line[0]):
                    if(key[1] == line[1]):
                        match = True

                if(match == True):
                    break

            if(match == True):
                sql = "SELECT i_name FROM Instructor WHERE (i_instrid = " + str(instructor_id) + " )"
                cursor.execute(sql)
                name = cursor.fetchall()

                print(f'\nLogin Successful! Welcome Professor {name[0][0]}!\n')
                session_type = 'Instructor'
                session_id = instructor_id
                session_name = name[0][0]

                return

            else: 
                print("Login Failed; Please make sure to enter a valid ID and password")

        else:
            print('Sorry, that is not a valid account type. Please try again.')

def options(conn):
    global session_type
    global session_id
    global session_name

    if(session_type == 'Student'):

        while(True):
            print("\nOptions:")
            print("1. View Current Grades")
            print("2. Log Out\n")

            choice = int(input("Please choose an option: "))

            if(choice == 1):

                sql = "SELECT c_name, e_grade FROM Enrollment, Classes WHERE (e_studentid = " + str(session_id) + ") AND (e_courseid = c_courseid)"
                
                cursor = conn.cursor()
                cursor.execute(sql)
                grades = cursor.fetchall()

                print('\n')

                for grade in grades:
                    print(f"Course: {grade[0]}        Grade: {grade[1]}")

            elif(choice == 2):
                print(f"Have a good day {session_name}!\nLogging Out...\n")
                break

            else:
                print("Sorry, this option does not exist. Please choose a valid option.")
                continue

    elif(session_type == 'Instructor'):

        while(True):
            print("\nOptions:")
            print("1. View Class Roster")
            print("2. View a Student Grades")
            print("3. Edit a Student's Grade")
            print("4. Remove a Student From Your Course")
            print("5. Log Out\n")

            choice = int(input("Please choose an option: "))

            if(choice == 1):

                sql = "SELECT c_name, s_name, s_studentid FROM Instructor, Classes , Student, Enrollment WHERE (s_studentid = e_studentid) AND (e_courseid = c_courseid) AND (c_instrid = i_instrid) AND (i_instrid = " + str(session_id) + ")"
                
                cursor = conn.cursor()
                cursor.execute(sql)
                students = cursor.fetchall()

                for student in students:
                    print(f"Course: {student[0]}        Student: {student[1]}        Student's ID: {student[2]}")

            elif(choice == 2):
                
                students_id = str(input("Please enter the id of the student whose grades you want to view: "))

                sql = "SELECT c_name, s_name, e_grade FROM Student, Enrollment, Classes, Instructor WHERE (s_studentid = " + students_id + ") AND (e_studentid = s_studentid) AND (e_courseid = c_courseid) AND (c_instrid = i_instrid) AND (i_instrid = " + str(session_id) + ")"                
                
                cursor = conn.cursor()
                cursor.execute(sql)
                student_grade = cursor.fetchall()

                if(len(student_grade) != 0):
                    for line in student_grade:
                        print(f"Course: {line[0]}        Student: {line[1]}        Grade: {line[2]}")
                
                else:
                    print("No search results returned; Student may not be in any of your classes")

            elif(choice == 3):

                sql = "SELECT c_name, s_name, s_studentid, e_grade FROM Instructor, Classes , Student, Enrollment WHERE (s_studentid = e_studentid) AND (e_courseid = c_courseid) AND (c_instrid = i_instrid) AND (i_instrid = " + str(session_id) + ")"
                
                cursor = conn.cursor()
                cursor.execute(sql)
                students = cursor.fetchall()

                for student in students:
                    print(f"Course: {student[0]}        Student: {student[1]}        Student's ID: {student[2]}")

                print('\n')

                print('Requesting Information of the Line to be Updated:')
                course = str(input("Please enter the name of the course: "))
                students_id = str(input("Please enter the Student's ID: "))
                new_grade =str(input("Please enter the new grade: "))

                sql = f"""UPDATE Enrollment
                 SET e_grade = {new_grade}
                 WHERE e_studentid = {students_id} AND e_courseid = 
                 (SELECT c_courseid 
                 FROM Classes 
                 WHERE c_name = '{course}')"""

                conn.execute(sql)

            elif(choice == 4):
                course = str(input("Please enter the name of the course that you wish to remove a student from: "))
                students_id = str(input("Please enter the id of the student you wish to remove: "))

                sql = "DELETE FROM Enrollment WHERE (e_studentid = " + students_id + ") AND (e_courseid = (SELECT c_courseid FROM Classes WHERE c_name = '" + course + "'))"

                conn.execute(sql)

            elif(choice == 5):
                print(f"Have a good day Professor {session_name}!\nLogging Out...\n")
                break

            else:
                print("Sorry, this option does not exist. Please choose a valid option.")
                continue


def main():
    database = r"studentgrade.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        dropTable(conn)
        createTable(conn)
        populateTable(conn)

        #Request Login
        login(conn)

        #Personalized Options for Students and Professors
        options(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
