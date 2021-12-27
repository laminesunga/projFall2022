insert into Classes (c_name,c_instrid,c_departid,c_description,c_capacity,c_enrollNumber,c_days,c_start_time,c_end_time)
values('MATH 100', '1','1','calculus 1','20', '4','Monday-Wednesday', '10:00 AM', '11:30 AM');


insert into Departement (d_name)
values('MATH');


insert into Enrollment (e_c_name,e_studentid,e_courseid,e_grade)
values ('MATH 100','1','1','92');


insert into instructor (i_name,i_username)
values ('Raph Jenkis','rj');


insert into Student (s_name,s_Username,s_phone,s_birthdate)
values('jose Santos','jsantos','800-000-0001','2000-01-23');
 

insert into users(Username,Password)
values('jsantos','w12');

insert into users(Username,Password)
values('rj','r12');

CREATE TABLE enrollment (
        e_Id INTEGER primary key autoincrement,
        e_cname VARCHAR (30) NOT NULL,
        e_studentid INTEGER NOT NULL,
        e_courseid INTEGER NOT NULL,
        e_grade FLOAT NOT NULL)