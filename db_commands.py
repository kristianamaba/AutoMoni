# import sqlite3
import json
import time
from asyncio.windows_events import NULL

import mysql.connector
from dateutil import parser
from flask import request, session

from utils import decrypt, getDateTime, hash, ranStr, saveJson, sendAsyncEmail

con = mysql.connector.connect(
    host=process.env.host, user=process.env.user, password=process.env.password, database=process.env.db
)


# CRUD NOTIF START


def checkNotif(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT a_notif_id FROM `a_notif_table` WHERE ac_id= %s	AND a_num= %s", value)
    entry = cur.fetchone()

    if entry is None:
        return True
    else:
        return False


def addNotif(value):
    sql = """INSERT INTO `a_notif_table` 
    (ac_id,a_num) 
    VALUES 
    ( %s,%s)"""

    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


# CRUD NOTIF END


def addChangeLog(value):
    value.append(getDateTime())
    sql = """INSERT INTO `changelog_tbl` 
    (ac_id,cl_desc,cl_date) 
    VALUES 
    ( %s,%s,%s)"""

    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


def addLoginLog(value):
    value.append(getDateTime())
    sql = """INSERT INTO `loginlogs_tbl` 
    (ac_id,ll_desc,ll_date) 
    VALUES 
    ( %s,%s,%s)"""

    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


# USER DATA
def getUserDataLive(s):
    con.reconnect()
    cur = con.cursor(buffered=True)
    sql = """SELECT randS,monintor_late_time,monitor_sched,monitor_sect,showcam, monitoring_type
    FROM `userdata_tbl` WHERE LOWER(`userdata_tbl`.`randS`) = LOWER(%s) AND monitoring = true"""
    cur.execute(sql, [s])
    entry = cur.fetchone()
    # field_names = [i[0] for i in cur.description]
    # return_dict = dict()
    # for idx, val in enumerate(field_names):
    #     return_dict [val] = entry[idx]
    # # dict["age"] = "20"
    # # dict["major"] = "Computer Science"

    return entry


def getUserData(s):
    con.reconnect()
    cur = con.cursor(buffered=True)
    sql = """SELECT *
    FROM `userdata_tbl` WHERE `userdata_tbl`.`randS` = %s"""
    cur.execute(sql, [s])
    entry = cur.fetchone()
    field_names = [i[0] for i in cur.description]
    return_dict = dict()
    for idx, val in enumerate(field_names):
        return_dict[val] = entry[idx]
    # dict["age"] = "20"
    # dict["major"] = "Computer Science"

    return return_dict

    # userdata = json.load(open('./userdata/'+s+'.json',))
    # return userdata


def changeUserData(s, ref, string):
    sql = """UPDATE `userdata_tbl` SET """ + ref + """ = %s WHERE `userdata_tbl`.`randS` = %s"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, [string, s])
    con.commit()

    # userdata = json.load(open('./userdata/'+s+'.json',))
    # userdata[ref] = string
    # saveJson(s,userdata,"userdata")


def createUserData(name):
    sql = """INSERT INTO `userdata_tbl` 
    (`randS`) 
    VALUES 
    ( %s)"""

    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, [name])
    con.commit()


# USER DATA

# REVISED


def get_menu(value):
    sql = """SELECT 
                m.Name, m.Href, m.Icon 
            FROM menu m 
            LEFT JOIN 
                menu_access ma ON m.menu_id = ma.menu_id 
            WHERE ma.ty_id = %s
            ORDER BY m.Sort"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


# ADMIN - START


def get_teachers(value):
    sql = """ SELECT ac_id, ac_name FROM `ac_tbl` WHERE ty_id = 2 AND is_a_active=1"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def edit_account(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        "SELECT * FROM  ac_tbl WHERE (ac_name=%s AND ac_email = %s AND dept_id = %s AND ty_id = %s AND is_a_active = %s AND ac_id = %s)",
        value,
    )
    entry = cur.fetchone()

    if entry is None:
        cur.execute(
            "UPDATE ac_tbl SET ac_name=%s , ac_email = %s, dept_id = %s, ty_id = %s,is_a_active = %s   WHERE ac_id = %s",
            value,
        )
        con.commit()
        return {"status": 1, "message": "Account Edited"}
    else:
        return {"status": 0, "message": "Nothing has changed"}


def get_account_details(value):
    sql = """ SELECT
                ac_id, ac_name, ac_email, ty_id,dept_id, is_a_active
            FROM 
                ac_tbl
            wHERE
                ac_id = %s """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchone()
    return rows


def edit_adv_set(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        """UPDATE settings_tbl
                SET set_value = (case when set_id = 1 then %s
                                    when set_id = 2 then %s
                                    when set_id = 3 then %s
                                end)
                WHERE set_id in (1, 2, 3)""",
        value,
    )
    con.commit()

    disableSubjectSchoolYear([])

    return {"status": 1, "message": "Settings Edited Edited"}
    # entry = cur.fetchone()

    # if entry is None:
    #     cur.execute("UPDATE ac_tbl SET ac_name=%s , ac_email = %s, dept_id = %s, ty_id = %s  WHERE ac_id = %s", value)
    #     con.commit()
    #     return {'status':1,'message':'Settings Edited Edited'}
    # else:
    #     return {'status':0,'message':'Nothing has changed'}


def get_adv_set():
    sql = """ SELECT set_name, set_value FROM settings_tbl order by set_id"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_loginlogs():
    sql = """ SELECT 
            DATE_FORMAT(a.ll_date, "%Y/%c/%d %H:%i %p"), b.ac_name, a.ll_desc 
        FROM loginlogs_tbl a 
        INNER JOIN ac_tbl b ON a.ac_id = b.ac_id """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_changelogs():
    sql = """ SELECT 
            DATE_FORMAT(a.cl_date, "%Y/%c/%d %H:%i %p"), b.ac_name, a.cl_desc 
        FROM changelog_tbl a 
        INNER JOIN ac_tbl b ON a.ac_id = b.ac_id """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_accounts_details(value):
    sql = """ SELECT 
            a.ac_id, a.ac_name, c.dept_name, b.ty_name 
        FROM 
            ac_tbl a 
        INNER JOIN 
            ac_type_tbl b ON a.ty_id = b.ty_id
        LEFT JOIN 
            department_tbl c ON a.dept_id = c.dept_id
        WHERE 
            a.is_a_active = %s """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, [value])
    con.commit()
    rows = cur.fetchall()
    return rows


def checkEmail(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        "SELECT ac_id,A.ty_id,ac_name,ac_email,ac_pass,ac_salt,C.href FROM ac_tbl A JOIN menu_home B ON A.ty_id = B.ty_id JOIN menu C ON B.menu_id = C.menu_id WHERE A.ac_email = %s AND A.is_a_active=1",
        [value[0]],
    )
    entry = cur.fetchone()

    return entry


def change_pass(value):
    con.reconnect()
    cur = con.cursor(buffered=True)

    # cur.execute('SELECT ac_id,A.ty_id,ac_name,ac_email,ac_pass,ac_salt,C.href FROM ac_tbl A JOIN menu_home B ON A.ty_id = B.ty_id JOIN menu C ON B.menu_id = C.menu_id WHERE A.ac_email = %s',[value[0]])
    entry = checkEmail([value[3]])

    if entry is None:
        return {"status": 0, "message": "Invalid Email/Password"}
    else:
        if value[1] != value[2]:
            return {"status": 0, "message": "Password Mismatch"}
        elif entry[4] == hash(entry[5], value[0]):
            salt = ranStr(64)
            spass = hash(salt, value[1])
            cur.execute(
                "UPDATE `ac_tbl` SET `ac_pass` = %s, `ac_salt` = %s WHERE `ac_tbl`.`ac_id` = %s",
                [spass, salt, entry[0]],
            )
            con.commit()
            return {"status": 1, "message": "Successfully Changed Password"}
        else:
            return {"status": 0, "message": "Invalid Email/Password"}


def check_account(value):
    con.reconnect()
    cur = con.cursor(buffered=True)

    # cur.execute('SELECT ac_id,A.ty_id,ac_name,ac_email,ac_pass,ac_salt,C.href FROM ac_tbl A JOIN menu_home B ON A.ty_id = B.ty_id JOIN menu C ON B.menu_id = C.menu_id WHERE A.ac_email = %s',[value[0]])
    entry = checkEmail([value[0]])

    if entry is None:
        return {"status": 0, "message": "Invalid Email/Password"}
    else:
        if entry[4] == hash(entry[5], value[1]):
            session["id"] = entry[0]
            session["ty"] = entry[1]
            session["name"] = entry[2]
            session["email"] = entry[3]

            session["randS"] = ranStr(6) + time.strftime("%Y%m%d_%H%M%S")
            randS = session["randS"]

            createUserData(session["randS"])
            changeUserData(randS, "id", entry[0])
            changeUserData(randS, "ty", entry[1])
            changeUserData(randS, "name", entry[2])
            changeUserData(randS, "email", entry[3])
            changeUserData(randS, "randS", randS)

            session["home"] = entry[6]
            session["menu"] = get_menu([entry[1]])
            session["loggedIn"] = True

            addLoginLog([entry[0], "Logged in"])

            return {"status": 1, "message": "Successfully Logged-In", "s": session["randS"]}
        else:
            return {"status": 0, "message": "Invalid Email/Password"}


def add_account(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT * FROM  ac_tbl WHERE (ac_email = %s)", [value[2]])
    entry = cur.fetchone()

    if entry is None:
        cur.execute(
            "INSERT INTO ac_tbl(ty_id,ac_name,ac_email,ac_pass,ac_salt,dept_id) VALUES(%s,%s,%s,%s,%s,%s)", value
        )
        con.commit()
        return {"status": 1, "message": "New Account added"}
    else:
        return {"status": 0, "message": "Account/Email already exists"}


def get_all_roles():
    sql = """ SELECT
                ty_id, ty_name
            FROM 
                ac_type_tbl """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql)
    con.commit()
    rows = cur.fetchall()
    return rows


# ADMIN - END


# SECTIONS PAGE FUNCTIONS - START


def edit_section(value):
    print(value)
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT * FROM  section_tbl WHERE (sect_name=%s AND sect_id != %s)", [value[0], value[2]])
    entry = cur.fetchone()

    if entry is None:
        cur.execute("UPDATE section_tbl SET sect_name = %s, is_se_active = %s WHERE sect_id = %s", value)
        con.commit()
        return {"status": 1, "message": "Section Edited"}
    else:
        return {"status": 0, "message": "Name already exists"}


def get_section_details(value):
    sql = """ SELECT
                sect_id, sect_name, is_se_active
            FROM 
                section_tbl 
            wHERE
                sect_id = %s"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def add_section(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT * FROM  section_tbl WHERE (sect_name=%s)", value)
    entry = cur.fetchone()

    if entry is None:
        cur.execute("INSERT INTO section_tbl(sect_name) VALUES(%s)", value)
        con.commit()
        return {"status": 1, "message": "New section added"}
    else:
        return {"status": 0, "message": "Name already exists"}


def get_sections_details(value):
    # SELECT
    #             a.sect_id, sect_name, COUNT(b.sect_id)
    #         FROM
    #             section_tbl a
    #             LEFT JOIN student_tbl b ON a.sect_id = b.sect_id
    #         WHERE is_se_active = %s
    #         GROUP BY a.sect_id
    sql = """ 
            SELECT
                a.sect_id, sect_name, COUNT(DISTINCT b.sect_id)
            FROM 
                section_tbl a 
            LEFT JOIN subject_registration_tbl b ON a.sect_id = b.sect_id 
            LEFT JOIN subject_tbl c ON b.subject_id = c.subject_id
            WHERE is_se_active = %s
            GROUP BY a.sect_id"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_sections_details_t(value):

    sql = """ SELECT
                a.sect_id, sect_name, COUNT(DISTINCT b.stud_id)
            FROM 
                section_tbl a
                INNER JOIN subject_registration_tbl b ON a.sect_id = b.sect_id 
                INNER JOIN subject_tbl c ON b.sect_id = c.sect_id
                INNER JOIN student_tbl d ON b.stud_id = d.stud_id
            WHERE a.ac_id = %s AND c.is_su_active = 1
            GROUP BY a.sect_id
            """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


# SECTIONS PAGE FUNCTIONS - END


# DEPARTMENTS PAGE FUNCTIONS - START
def get_departments(value):
    sql = """ SELECT dept_id, dept_name FROM department_tbl WHERE is_d_active=1"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def edit_department(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT * FROM  department_tbl WHERE (dept_name=%s AND dept_id != %s)", [value[0], value[2]])
    entry = cur.fetchone()

    if entry is None:
        cur.execute("UPDATE department_tbl SET dept_name = %s, is_d_active = %s WHERE dept_id = %s", value)
        con.commit()
        return {"status": 1, "message": "Department Edited"}
    else:
        return {"status": 0, "message": "Name already exists"}


def get_department_details(value):
    sql = """ SELECT
                dept_id, dept_name, is_d_active
            FROM 
                department_tbl 
            wHERE
                dept_id = %s"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def add_department(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT * FROM  department_tbl WHERE (dept_name=%s)", value)
    entry = cur.fetchone()

    if entry is None:
        cur.execute("INSERT INTO department_tbl(dept_name) VALUES(%s)", value)
        con.commit()
        return {"status": 1, "message": "New department added"}
    else:
        return {"status": 0, "message": "Name already exists"}


def get_departments_details(value):

    sql = """ SELECT A.dept_id, A.dept_name, count(B.dept_id) as teachers, (SELECT count(*) FROM subject_tbl C WHERE C.dept_id = A.dept_id) AS subjects
                FROM department_tbl A 
                LEFT JOIN ac_tbl B ON A.dept_id = B.dept_id
                WHERE A.is_d_active=%s
                GROUP BY A.dept_id"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


# DEPARTMENTS PAGE FUNCTIONS - END


# SUBJECT PAGE FUNCTIONS - START
def get_all_subj_management(value):
    sql = """ SELECT
                a.subject_id, subject_name, b.sect_name, c.year_text
            FROM 
                subject_tbl a
                LEFT JOIN section_tbl b ON a.sect_id = b.sect_id 
                INNER JOIN year_tbl c ON a.acad_year = c.year_id
            WHERE
                a.is_su_active = 1"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_all_subj(value):
    sql = """ SELECT
                a.subject_id, subject_name, b.sect_name, c.year_text
            FROM 
                subject_tbl a
                LEFT JOIN section_tbl b ON a.sect_id = b.sect_id
                INNER JOIN year_tbl c ON a.acad_year = c.year_id
            WHERE 
                a.ac_id = %s 
                AND a.is_su_active = 1"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def edit_subject(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        "SELECT * FROM  subject_tbl WHERE (subject_name=%s AND dept_id = %s AND sect_id = %s AND acad_year = %s AND ac_id = %s AND is_su_active = %s AND subject_id = %s  )",
        value,
    )
    entry = cur.fetchone()

    if entry is None:
        cur.execute(
            "UPDATE subject_tbl SET subject_name=%s ,dept_id = %s, sect_id = %s , acad_year = %s, ac_id = %s, is_su_active = %s WHERE subject_id = %s",
            value,
        )
        con.commit()
        return {"status": 1, "message": "Subject Edited"}
    else:
        return {"status": 0, "message": "Nothing is Changed"}


def get_subject_details(value):
    sql = """ SELECT
                subject_id, subject_name,  sect_id,acad_year, ac_id,dept_id, is_su_active
            FROM 
                subject_tbl
            wHERE
                subject_id = %s """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def add_subject(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        "SELECT * FROM  subject_tbl WHERE (subject_name=%s AND dept_id = %s AND sect_id = %s AND acad_year = %s AND ac_id = %s)",
        value,
    )
    entry = cur.fetchone()

    if entry is None:
        # if(acad_year=(SELECT set_value FROM settings_tbl WHERE set_id=3), 1, 0)
        value.append(value[3])
        cur.execute(
            "INSERT INTO subject_tbl(subject_name,dept_id,sect_id,acad_year,ac_id,is_su_active) VALUES(%s,%s,%s,%s,%s,if(%s=(SELECT set_value FROM settings_tbl WHERE set_id=3), 1, 0))",
            value,
        )
        con.commit()
        return {"status": 1, "message": "New Subject added"}
    else:
        return {"status": 0, "message": "Name already exists"}


def get_subjects_details(value):

    sql = """ SELECT 
                a.subject_id, subject_name, d.dept_name, c.ac_name, b.sect_name, e.year_text, c.ac_id, b.sect_id, c.ac_email
            FROM 
                subject_tbl a 
            LEFT JOIN 
                section_tbl b ON a.sect_id = b.sect_id
            INNER JOIN department_tbl d ON a.dept_id = d.dept_id
            INNER JOIN 
                ac_tbl c ON a.ac_id = c.ac_id
            INNER JOIN year_tbl e ON a.acad_year = e.year_id
            WHERE
                is_su_active = %s
            """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_subjects_details_t(value):

    sql = """ SELECT 
                a.subject_id, subject_name, d.dept_name, c.ac_name, b.sect_name, e.year_text
            FROM 
                subject_tbl a 
            LEFT JOIN 
                section_tbl b ON a.sect_id = b.sect_id
            INNER JOIN department_tbl d ON a.dept_id = d.dept_id
            INNER JOIN 
                ac_tbl c ON a.ac_id = c.ac_id
            INNER JOIN year_tbl e ON a.acad_year = e.year_id
            WHERE a.ac_id = %s AND a.is_su_active=1
            """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


# SUBJECT PAGE FUNCTIONS - END


def disableSubjectSchoolYear(value):
    sql = """ UPDATE subject_tbl a SET a.is_su_active = if(acad_year=(SELECT set_value FROM settings_tbl WHERE set_id=3), 1, 0)"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


# SECTION SPECIFIC PAGE FUNCTIONS - START


def changeStudId(value):
    sql = """ UPDATE `student_tbl` SET `stud_id_text` = %s WHERE `stud_id` = %s """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


def add_student_management(value, subjects, key, studId):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        "SELECT * FROM  student_tbl WHERE (stud_email=%s AND stud_email != '') ||  (stud_id_text=%s AND stud_id_text != '') ",
        [value[1], studId],
    )
    entry = cur.fetchone()

    if entry is None:
        cur.execute("INSERT INTO student_tbl(stud_name,stud_email) VALUES(%s,%s)", value)
        con.commit()
        stud_id = cur.lastrowid
        studIdText = studId if studId != "" else ranStr(5) + str(123 + stud_id)
        changeStudId([studIdText, stud_id])
        for row in subjects:
            subj_id = decrypt(row, key)
            sect_id = getSectId([subj_id])
            register_subj_sect_stud([stud_id, sect_id, subj_id])
        return {"status": 1, "message": "New student added"}
    else:
        return {"status": 0, "message": "Email already exists"}


def add_student(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT * FROM  student_tbl WHERE (stud_name=%s AND sect_id=%s)", [value[0], value[1]])
    entry = cur.fetchone()

    if entry is None:
        cur.execute("INSERT INTO student_tbl(stud_name,sect_id,stud_email) VALUES(%s,%s,%s)", value)
        con.commit()
        return {"status": 1, "message": "New student added"}
    else:
        return {"status": 0, "message": "Name already exists"}


def get_sectid_byname(value):
    sql = """SELECT a.sect_id, a.sect_name FROM section_tbl a WHERE a.sect_id = %s"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchone()

    return rows


# def get_sectid_byname(value):
#     sql = '''SELECT a.sect_id FROM section_tbl a WHERE a.sect_name = %s AND a.ac_id = %s '''
#     con.reconnect()
#     cur = con.cursor(buffered=True)
#     cur.execute(sql,value)
#     con.commit()
#     rows = cur.fetchone()[0]

#     return rows


def get_all_students(value):
    sql = """SELECT
        b.stud_id, b.stud_name, b.stud_email, SUM(if(d.is_su_active = 1, 1,0)), b.stud_id_text
        FROM student_tbl b
        LEFT JOIN subject_registration_tbl c ON b.stud_id = c.stud_id
        LEFT JOIN section_tbl a ON a.sect_id = c.sect_id
        LEFT JOIN subject_tbl d ON d.subject_id = c.subject_id  
        WHERE b.is_st_active = %s 
        GROUP BY b.stud_id
            """
    #
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()

    return rows


def get_sect_students(value):
    sql = """SELECT
                b.stud_id, B.stud_name, COUNT(DISTINCT d.p_id), b.stud_id_text, b.stud_email
            FROM student_tbl b
            LEFT JOIN subject_registration_tbl c ON b.stud_id = c.stud_id
            LEFT JOIN section_tbl a ON a.sect_id = c.sect_id
            LEFT JOIN photo_tbl d ON b.stud_id = d.stud_id
            WHERE a.sect_id = %s
            GROUP BY b.stud_id
            """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()

    return rows


# DELETE FROM table WHERE search_condition


# SECTION SPECIFIC PAGE FUNCTIONS - END


def check_subj_sect_stud(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    sql = "SELECT sr_id FROM `subject_registration_tbl` WHERE `stud_id` = %s AND `sect_id` = %s AND `subject_id` = %s"
    cur.execute(sql, value)

    rows = cur.fetchall()

    for row in rows:
        return row[0]

    return 0


def register_subj_sect_stud(value):
    if check_subj_sect_stud(value) == 0:
        sql = """INSERT INTO
        `subject_registration_tbl` (`stud_id`, `sect_id`, `subject_id`)
        VALUES (%s, %s, %s); """
        con.reconnect()
        cur = con.cursor(buffered=True)
        cur.execute(sql, value)
        con.commit()
    # else:
    #     tempArr = list(value)
    #     tempArr.append(value[0])
    #     tempArr.append(value[1])
    #     sql = """ UPDATE attendance_tbl SET sched_id = %s, stud_id= %s, att_time= %s, att_stat= %s, subject_id = %s, is_validated = %s WHERE sched_id=%s AND stud_id=%s """
    #     con.reconnect()
    #     cur = con.cursor(buffered=True)
    #     cur.execute(sql, tempArr)
    #     con.commit()


def getSectId(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    sql = "SELECT sect_id FROM `subject_tbl` WHERE `subject_id` = %s"
    cur.execute(sql, value)

    rows = cur.fetchall()

    for row in rows:
        return row[0]

    return 0


def edit_student_management(value, value2, value3, key):
    tempArray = value[:-2]
    tempArray.append(value[-1])
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        "SELECT * FROM  student_tbl WHERE (stud_name=%s AND stud_email != %s AND stud_id != %s)",
        tempArray,
    )
    entry = cur.fetchone()

    if entry is None:
        cur.execute(
            "UPDATE student_tbl SET stud_name = %s, stud_email = %s, is_st_active = %s WHERE stud_id = %s", value
        )
        con.commit()
        for row in value2:
            cur.execute("INSERT INTO photo_tbl(stud_id,p_name) VALUES(%s,%s)", [value[3], row])
            con.commit()

        for row in value3:
            subj_id = decrypt(row, key)
            sect_id = getSectId([subj_id])
            register_subj_sect_stud([value[3], sect_id, subj_id])

        return {"status": 1, "message": "Student Edited"}
    else:
        return {"status": 0, "message": "Name Already exists"}


def edit_student(value, value2):
    con.reconnect()
    cur = con.cursor(buffered=True)
    for row in value2:
        cur.execute("INSERT INTO photo_tbl(stud_id,p_name) VALUES(%s,%s)", [value[0], row])
        con.commit()
    return {"status": 1, "message": "Photos Saved"}


def delete_student_photos(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("""SELECT p_name FROM photo_tbl WHERE stud_id = %s""", value)
    con.commit()
    rows = cur.fetchall()

    cur.execute("""DELETE FROM photo_tbl WHERE stud_id = %s""", value)
    con.commit()
    return rows


def get_student_details_rev(value):
    sql = """SELECT b.stud_id, b.stud_name, COUNT(DISTINCT p_id) as p_c, b.stud_email,
            GROUP_CONCAT(DISTINCT aa.subject_id) as subs_ids,
            b.is_st_active
            FROM student_tbl b
            LEFT JOIN subject_registration_tbl aa on aa.stud_id = b.stud_id
            LEFT JOIN section_tbl a ON a.sect_id = aa.sect_id
            LEFT JOIN photo_tbl c ON b.stud_id = c.stud_id 
            LEFT JOIN subject_tbl d ON aa.subject_id = d.subject_id
            WHERE b.stud_id = %s AND d.is_su_active = 1"""
    # sql = """SELECT b.stud_id, stud_name, COUNT(DISTINCT p_id) as p_c, b.stud_email,
    #         GROUP_CONCAT(DISTINCT aa.subject_id) as subs_ids,
    #         b.is_st_active
    #         FROM section_tbl a
    #         INNER JOIN subject_registration_tbl aa on a.sect_id = aa.sect_id
    #         INNER JOIN student_tbl b ON aa.stud_id = b.stud_id
    #         LEFT JOIN photo_tbl c ON b.stud_id = c.stud_id
    #         INNER JOIN subject_tbl d ON aa.subject_id = d.subject_id
    #         WHERE b.stud_id = %s AND d.is_su_active = 1
    #         GROUP BY b.stud_id"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_student_email(value):
    sql = """SELECT
                b.stud_id, stud_name, COUNT(c.stud_id), b.stud_email
            FROM 
                section_tbl a
            INNER JOIN subject_registration_tbl aa on a.sect_id = aa.sect_id
            INNER JOIN student_tbl b ON aa.stud_id = b.stud_id
            LEFT JOIN photo_tbl c ON b.stud_id = c.stud_id
            WHERE b.stud_id = %s AND a.sect_id = %s
            GROUP BY b.stud_id"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    for row in rows:
        return row[3]

    return ""


def get_student_details(value):
    sql = """SELECT
                b.stud_id, stud_name, COUNT(c.stud_id), b.stud_email
            FROM 
                section_tbl a
            INNER JOIN subject_registration_tbl aa on a.sect_id = aa.sect_id
            INNER JOIN student_tbl b ON aa.stud_id = b.stud_id
            LEFT JOIN photo_tbl c ON b.stud_id = c.stud_id
            WHERE b.stud_id = %s AND a.sect_id = %s
            GROUP BY b.stud_id"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows

    # rows = cur.fetchall()
    # for row in rows:
    #     return row[0]

    # return 0


def get_section_id(value):
    sql = """SELECT
                a.sect_id
            FROM 
                section_tbl a
            WHERE a.sect_name = %s AND ac_id = %s """
    # print(value)
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchone()[0]
    # print(rows)
    return rows


def get_stud_subjects_details(value):
    sql = """SELECT C.subject_id, concat_ws(" ",C.subject_name, "-", E.sect_name ,"(",F.year_text,")") as SubName, D.ac_id, D.ac_name, D.ac_email, A.stud_id, A.stud_name
            FROM student_tbl A
            INNER JOIN subject_registration_tbl B ON A.stud_id = B.stud_id
            INNER JOIN subject_tbl C ON B.subject_id = C.subject_id
            INNER JOIN ac_tbl D ON C.ac_id = D.ac_id
            INNER JOIN section_tbl E ON C.sect_id = E.sect_id
            INNER JOIN year_tbl F ON C.acad_year = F.year_id
            WHERE A.stud_email = %s AND A.stud_id_text = %s AND C.is_su_active=1"""
    # print(value)
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_stud_att_sum(value):
    sql = (
        """SELECT stud_name """
        + getColFormat([value[0], value[1]], 1)
        + """
            FROM student_tbl A
            INNER JOIN subject_registration_tbl AA ON A.stud_id = AA.stud_id
            INNER JOIN subject_tbl E ON AA.subject_id = E.subject_id
            INNER JOIN section_tbl D ON E.sect_id = D.sect_id
            INNER JOIN sched_tbl B ON B.subject_id = E.subject_id
            LEFT JOIN attendance_tbl C ON B.sched_id = C.sched_id AND A.stud_id = C.stud_id
            WHERE
                E.subject_id = %s AND A.stud_id = %s
            GROUP BY A.stud_id"""
    )
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, [value[0], value[2]])
    con.commit()
    rows = cur.fetchall()
    return rows


def get_pending_sched_id(value):
    sql = """ SELECT B.subject_id
            FROM sched_tbl A
            INNER JOIN subject_tbl B ON B.subject_id = A.subject_id
            WHERE A.sched_id = %s 
            AND A.ac_id = %s 
            AND A.monitoring_stage = 1
                """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    for row in rows:
        return row[0]

    return 0


def get_pending_attendance(value):
    sql = """ SELECT B.sched_id, E.subject_name, D.sect_name, DATE_FORMAT(B.sched_time, "%b %d, %Y")
                FROM section_tbl D
                INNER JOIN subject_tbl E ON D.sect_id = E.sect_id
                INNER JOIN sched_tbl B ON B.subject_id = E.subject_id
                INNER JOIN attendance_tbl C ON B.sched_id = C.sched_id
                WHERE
                B.monitoring_stage = 1
                AND
                B.ac_id = %s
                GROUP BY B.sched_id
                """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_attendance(section, type):
    sql = (
        """SELECT A.stud_id, stud_name """
        + getColFormat(section, type)
        + """
            FROM student_tbl A
            INNER JOIN subject_registration_tbl AA ON AA.stud_id = A.stud_id
            INNER JOIN subject_tbl E ON AA.subject_id = E.subject_id
            INNER JOIN section_tbl D ON E.sect_id = D.sect_id
            INNER JOIN sched_tbl B ON B.subject_id = E.subject_id
            LEFT JOIN attendance_tbl C ON B.sched_id = C.sched_id AND A.stud_id = C.stud_id
            WHERE
                """
        + (" E.subject_id = %s " if type == 1 else " YEAR(B.sched_time) = %s AND MONTH(B.sched_time) = %s ")
        + """ 
                AND A.ac_id = %s
            GROUP BY A.stud_id"""
    )
    # LEFT JOIN attendance_tbl

    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, section)
    con.commit()
    rows = cur.fetchall()
    return rows


# INNER JOIN section_tbl D ON A.sched_sect = D.sect_id
def get_headers(section, type):
    sql = (
        """SELECT DISTINCT a.sched_id, b.att_time 
            FROM sched_tbl A
            JOIN attendance_tbl B ON A.sched_id = B.sched_id
            INNER JOIN subject_tbl E ON A.subject_id = E.subject_id
            WHERE
                 """
        + (" E.subject_id = %s " if type == 1 else " YEAR(A.sched_time) = %s AND MONTH(A.sched_time) = %s ")
        + """ 
                 AND A.ac_id = %s
            GROUP BY  A.sched_id
            ORDER BY A.sched_id DESC
            """
    )
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, section)
    con.commit()
    rows = cur.fetchall()
    returnTemp = []
    for idx, val in enumerate(rows):
        returnTemp.append([val[0], parser.parse(str(val[1])).strftime("%b %d,%Y")])
        # returnTemp.append([val[0],parser.parse(val[1]).strftime('%b %d,%Y %H:%M %p')])

    return returnTemp


def getColFormat(section, type):
    stringAll = ""
    headers = get_headers(section, type)
    for row in headers:
        # stringAll += ", sum(CASE WHEN C.sched_id IS '"+str(row[0])+"' THEN att_stat ELSE 0 END) as a"+str(row[0])+"";
        stringAll += (
            ", sum(if (C.sched_id = '" + str(row[0]) + "' AND is_validated=1,att_stat,0)) as a" + str(row[0]) + ""
        )
    # for ($i = 0; $i < count($headers); $i++) if (b.subject_id = 1, (att_stat / 2), att_stat)
    # 	stringAll .= ", sum(if(C.da_id='".$headers[$i]->da_id."',A.mo_slp,0)) '".$headers[$i]->da_id."'";
    return stringAll


def get_marked_attendance(value):
    sql = """ SELECT c.att_id, a.stud_name, DATE_FORMAT(c.att_time, "%b %d, %Y %h:%i %p"),c.att_stat
                FROM student_tbl a
                INNER JOIN subject_registration_tbl aa ON a.stud_id = aa.stud_id
               	INNER JOIN subject_tbl b ON aa.sect_id = b.sect_id
                INNER JOIN attendance_tbl c ON a.stud_id = c.stud_id
                WHERE 
                c.sched_id=%s AND c.subject_id = %s AND c.att_id > %s
     """
    # print(value)
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    rows = cur.fetchall()
    con.commit()
    return rows


def update_monitoring_stat(value):
    sql = """ UPDATE `sched_tbl` SET `monitoring_stage` = '2' WHERE `sched_tbl`.`sched_id` = %s """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


def get_verified_attendance(value):
    sql = """ SELECT c.att_id, a.stud_name, DATE_FORMAT(c.att_time, "%b %d, %Y %h:%i %p"),c.att_stat
                FROM student_tbl a
                INNER JOIN subject_registration_tbl aa ON a.stud_id = aa.stud_id
               	INNER JOIN subject_tbl b ON aa.sect_id = b.sect_id
                INNER JOIN attendance_tbl c ON a.stud_id = c.stud_id
                WHERE 
                c.sched_id=%s AND c.subject_id = %s AND c.att_id > %s AND c.is_validated=1
     """
    # print(value)
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    rows = cur.fetchall()
    con.commit()
    return rows


def get_with_attendance(value):
    sql = """ SELECT a.stud_id, a.stud_name, c.att_stat, c.is_validated
                FROM student_tbl a
                INNER JOIN subject_registration_tbl aa ON a.stud_id = aa.stud_id
                INNER JOIN subject_tbl b ON aa.sect_id = b.sect_id
                INNER JOIN attendance_tbl c ON a.stud_id = c.stud_id
                WHERE 
                c.sched_id=%s AND b.subject_id = %s
                GROUP BY a.stud_id
     """

    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_no_attendance(value):
    sql = """ SELECT a.stud_id, a.stud_name 
                FROM student_tbl a
                INNER JOIN subject_registration_tbl aa ON a.stud_id = aa.stud_id
               	INNER JOIN subject_tbl b ON aa.sect_id = b.sect_id
                WHERE 
                a.stud_id NOT IN (
                    SELECT a.stud_id FROM attendance_tbl a 
                    WHERE a.sched_id=%s
                    GROUP BY a.stud_id
                ) AND b.subject_id = %s
     """

    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_sect_ref(value):
    sql = """ SELECT
                b.stud_id,
                stud_name,
                p_name
            FROM 
                section_tbl a
                INNER JOIN subject_registration_tbl aa ON a.sect_id = aa.sect_id
                INNER JOIN student_tbl b ON b.stud_id = aa.stud_id
                INNER JOIN photo_tbl c ON b.stud_id = c.stud_id
                INNER JOIN subject_tbl d ON aa.subject_id = d.subject_id
            WHERE
                d.subject_id = %s """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


# sched_sect
def get_schedules(value):
    sql = """ SELECT
                sched_id, sched_time
            FROM 
                sched_tbl
            WHERE
                subject_id = %s 
            ORDER BY 
                sched_id DESC"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_all_year(value):
    sql = """ SELECT
                year_id, year_text
            FROM 
                year_tbl"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def get_all_sect(value):
    sql = """ SELECT
                sect_id, sect_name
            FROM 
                section_tbl 
            WHERE
                is_se_active = 1 """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()
    rows = cur.fetchall()
    return rows


def create_sched(value):
    sql = """ INSERT INTO sched_tbl(subject_id,sched_time,ac_id, monitoring_stage)
              VALUES(%s,%s,%s,1) """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()

    return cur.lastrowid


def check_stud(value, type):
    con.reconnect()
    cur = con.cursor(buffered=True)
    sql = ""
    if type == 1:
        sql = "SELECT att_id FROM attendance_tbl WHERE sched_id=%s AND stud_id=%s"
    elif type == 2:
        sql = "SELECT att_id FROM attendance_tbl WHERE sched_id=%s AND stud_id=%s AND is_validated=0"
    cur.execute(sql, value)

    rows = cur.fetchall()

    for row in rows:
        return row[0]

    return 0


def validate_att(value):
    sql = """ UPDATE attendance_tbl SET is_validated = 1 WHERE att_id=%s AND is_validated = 0 """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


def get_stud_email_sub_att(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        """SELECT c.stud_name, c.stud_email, b.subject_name
            FROM attendance_tbl a
            INNER JOIN subject_tbl b ON a.subject_id - b.subject_id
            INNER JOIN student_tbl c ON a.stud_id = c.stud_id
            WHERE a.att_id = %s
            GROUP BY a.att_id""",
        value,
    )

    rows = cur.fetchall()

    for row in rows:
        return row[0]

    return 0


def mark_stud(value):
    if check_stud([value[0], value[1]], 1) == 0:
        sql = """ INSERT INTO attendance_tbl(sched_id, stud_id, att_time, att_stat,subject_id, is_validated)
                VALUES(%s,%s,%s,%s,%s,%s) """
        con.reconnect()
        cur = con.cursor(buffered=True)
        cur.execute(sql, value)
        con.commit()

        # att_id = cur.lastrowid
        # att_stat = ["Absent", "Present", "Late", "Excused"]
        # stud_details = get_stud_email_sub_att([att_id])
        # content = (
        #     "<table> <tbody> <tr> <td >Hi "
        #     + stud_details[0]
        #     + ",</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >You have been automatically marked as "
        #     + (att_stat[int(value[3])])
        #     + "</a></td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >On Time: "
        #     + value[2]
        #     + "</td> <td >Subject: "
        #     + stud_details[2]
        #     + "</td></tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Thanks,</td> </tr> <tr> <td >AutoMoni</td> </tr><tr> <td><br><br>DO NOT REPLY, THIS IS AN AUTOMATED MESSAGE</td> </tr> </tbody> </table>"
        # )
        # sendAsyncEmail("Attendance Mark ", stud_details[0], stud_details[1], content)
    else:
        tempArr = list(value)
        tempArr.append(value[0])
        tempArr.append(value[1])
        sql = """ UPDATE attendance_tbl SET sched_id = %s, stud_id= %s, att_time= %s, att_stat= %s, subject_id = %s, is_validated = %s WHERE sched_id=%s AND stud_id=%s """
        con.reconnect()
        cur = con.cursor(buffered=True)
        cur.execute(sql, tempArr)
        con.commit()


# Dashboard


def get_dashboard_det(id):
    sql = """SELECT  (
                SELECT COUNT(*)
                FROM   student_tbl a
                INNER JOIN subject_registration_tbl b ON a.stud_id = b.stud_id
                INNER JOIN subject_tbl c ON b.subject_id = c.subject_id
                WHERE c.ac_id = %s AND is_st_active=1
            ) AS a1,
            (
                SELECT COUNT(DISTINCT a.sect_id)
                FROM section_tbl a
                INNER JOIN subject_registration_tbl b ON a.sect_id = b.sect_id
                INNER JOIN subject_tbl c ON b.subject_id = c.subject_id
                WHERE c.ac_id = %s AND is_se_active=1
            ) AS a2,
            (
                SELECT COUNT(*)
                FROM   sched_tbl
                WHERE ac_id = %s
            ) AS a3,
            (
                SELECT COUNT(*)
                FROM   subject_tbl
                WHERE ac_id = %s AND is_su_active=1
            ) AS a4"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, [id, id, id, id])
    con.commit()
    rows = cur.fetchone()

    return rows


# OLD CODES


def add_sect(value):
    sql = """ INSERT INTO section_tbl(sect_name)
              VALUES(%s) """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


def add_stud(value):
    sql = """ INSERT INTO student_tbl(stud_name,sect_id)
              VALUES(%s,%s) """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


def edit_sect(value):
    sql = """ UPDATE section_tbl
                  SET sect_name = %s 
                  WHERE sect_name = %s"""
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


def edit_stud(value):
    sql = """ UPDATE student_tbl
                  SET stud_name = %s 
                  WHERE stud_name = %s AND sect_id = %s """
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(sql, value)
    con.commit()


def att_value(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        """SELECT B.stud_name, sum(if (att_stat = 1 , 1 , 0)),
                    sum(if (att_stat = 2, 1, 0)),
                    sum(if (att_stat = 3, 1, 0))
                    FROM attendance_tbl as A
                    INNER JOIN student_tbl as B on A.stud_id = B.stud_id
                    WHERE A.sect_id=%s
                    GROUP BY A.stud_id""",
        value,
    )

    rows = cur.fetchall()

    return rows


def sched_count(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT count(*) FROM sched_tbl WHERE subject_id=%s", value)

    rows = cur.fetchall()

    for row in rows:
        return row[0]

    return 0


def sched_all_sect(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT sched_id, sched_time FROM sched_tbl WHERE subject_id=%s", value)

    rows = cur.fetchall()

    return rows


def sched_all_stud(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT stud_id, stud_name FROM student_tbl WHERE sect_id=%s", value)

    rows = cur.fetchall()

    return rows


def att_per_stud(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT sched_id, att_stat,att_time FROM attendance_tbl WHERE sect_id=%s AND stud_id=%s", value)

    rows = cur.fetchall()

    return rows


def get_sect_id(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT sect_id FROM section_tbl WHERE sect_name=%s", (value,))

    rows = cur.fetchall()

    for row in rows:
        return row[0]

    return 0


def get_stud_name(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(
        "SELECT stud_name FROM student_tbl A INNER JOIN subject_tbl B ON A.sect_id = B.sect_id WHERE stud_id=%s AND B.subject_id = %s ",
        value,
    )

    rows = cur.fetchall()

    for row in rows:
        return row[0]

    return 0


def check_att_arr(val, arr):
    for row in arr:
        if val == row[0]:
            return [row[1], row[2]]
    return 0


def get_ids_on_att(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT stud_id FROM attendance_tbl WHERE sched_id=%s", (value,))

    rows = cur.fetchall()

    Temp = ""
    for i in rows:
        Temp += "," + str(i[0])

    return "(" + Temp[1:] + ")"


def get_stud_no_att(value):

    Cond = get_ids_on_att(value[1])
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT stud_id, stud_name FROM student_tbl WHERE stud_id NOT IN " + Cond + " AND sect_id=" + value[0])

    rows = cur.fetchall()

    return rows


def get_def_late():
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute("SELECT set_val FROM set_tbl WHERE set_id=2")

    rows = cur.fetchall()

    for row in rows:
        return row[0]

    return 0


def set_def_late(value):
    con.reconnect()
    cur = con.cursor(buffered=True)
    cur.execute(""" UPDATE set_tbl SET set_val = %s WHERE set_id=2""", value)
    con.commit()
