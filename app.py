import base64
import codecs
import io
import json
import logging
import os.path
import threading
import time
from datetime import datetime, timedelta
from importlib import reload
from sys import stdout
from turtle import up
from urllib.parse import parse_qs, urlparse

import cv2

# sys.path.append(".\env\Lib\site-packages")
# print(sys.path)
import face_recognition as fr
import mysql.connector
import numpy as np
import pytz
import requests
from dateutil.relativedelta import relativedelta
from engineio.payload import Payload
from flask import Flask, Response, render_template, request, session
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from imageio import imread
from PIL import Image

from db_commands import *

# from camera import Camera
from utils import *

utc = pytz.UTC
import faulthandler

Payload.max_decode_packets = 500
import gc

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.logger.addHandler(logging.StreamHandler(stdout))
app.config["SECRET_KEY"] = "secret!"
app.config["DEBUG"] = True
socketio = SocketIO(app, cors_allowed_origins="*")
# camera = Camera(Makeup_artist())

faulthandler.enable()
net = cv2.dnn.readNet("./Weights/yolov3_training_last.weights", "./Weights/yolov3_testing.cfg")
output_layers_names = net.getUnconnectedOutLayersNames()

# con = sqlite3.connect("system_db", check_same_thread=False)


# con = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
#   database="attendance_db"
# )

# from multiprocessing.dummy import Pool

# pool = Pool(10)
# "s"=>$subject,
# 				"to"=>$toEmail,
# 				"m"=>$content);

# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
#     }


# from httplib2 import Http
# from urllib.parse import urlencode

# subject = "something testubg"
# toEmail = "kristianamaba.kka@gmail.com"
# content = "testinggg"
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77'
#     }
# h = Http()
# data = dict(fromName="AutoMoni System",toName="AutoMoni User",toEmail=toEmail,content=content)
# resp, content =h.request("http://localhost/c/index.php/Main_controller/sendEmailPost", "POST", urlencode(data),headers=headers)
# print(content)

key = 22
ErrorString = '{"status": "0", "message": "ERROR: Something went wrong"}'


# dir = "./photos"
# for name in os.listdir(dir):
# #     saveJson('name',known_face_names,'photos')
# # for row in ref:
#     encoded_image = fr.load_image_file(dir + "/" + name)
#     if (len(fr.face_encodings(encoded_image)) >= 1):
#         face_encoding = fr.face_encodings(encoded_image)[0].tolist()
#         saveJson(name[:-4],face_encoding,'photos')
@app.route("/")
@app.route("/<link>")
@app.route("/<link>/<slink>")
def redirectTo(link="login", slink=""):
    if link == "student_details":
        return render_template(link + ".html")
    if link == "monitoring" and slink != "":
        # slink = decrypt(slink, key)
        session["live-list"] = []
        return render_template("monitoring_students.html", data=slink)
    elif session.get("loggedIn") == True:
        session["linkReal"] = link

        data = []

        if link == "logout":
            link = "login"
            session.clear()
            return render_template("login.html")
        if os.path.isfile("./templates/" + link + ".html") is not True and link != "login":
            link = session["home"]
        session["linkTabs"] = link

        return render_template(link + ".html", profileDropdown=profileDropdown(), menubar=menubar(), data=data)
    else:
        return render_template("login.html")


# session['id']

# DECODE fernet.decrypt(encMessage).decode()


@app.route("/crud/<link>", methods=["POST", "GET"])
@cross_origin()
def handle_data(link):

    parsed_url = urlparse(request.url)
    # print(parsed_url)
    token = None
    userdata = None
    if link == "login_account":
        return json.dumps(check_account([request.form["email"], request.form["pass"]]))
    elif link == "get_stud_att_details":
        tempReturn = []
        subDetails = get_stud_subjects_details([request.form["email"], request.form["studId"]])

        for idx, val in enumerate(subDetails):
            tempReturn.append(
                {
                    "data": val,
                    "header": get_headers([val[0], val[2]], 1),
                    "attendance": get_stud_att_sum([val[0], val[2], val[5]]),
                }
            )

        if len(subDetails) == 0:
            return '{"status": "0", "message": "Student not found."}'
        else:
            return (
                '{"status": "1", "message": "Successfully Found Student Details", "data":'
                + json.dumps(tempReturn, cls=DecimalEncoder)
                + "}"
            )
        # print(get_stud_att_sum([userdata['secttion_a_id'], request.form['s']]))
        # tempReturn.append(get_headers([userdata["secttion_a_id"], userdata["id"]], 1))
        # return json.dumps(tempReturn, cls=DecimalEncoder)
    elif "s" in parse_qs(parsed_url.query):
        token = parse_qs(parsed_url.query)["s"][0]
        userdata = getUserData(token)
        if len(userdata) == 0:
            return '{"status": "0", "message": "Unauthorized"}'
    else:
        return '{"status": "0", "message": "Unauthorized"}'
    # changeUserData(token, '', string):

    try:

        # print(parse_qs(parsed_url.query)['sample'][0])
        # print(parse_qs(parsed_url.query)['sample'][0])
        if link == "get_pending_attendance":
            return (
                '{"status": "1", "message": "Successfully Loaded Pending Attendance", "data":'
                + json.dumps(get_pending_attendance([userdata["id"]]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "continue_pending_monitoring":
            if userdata["monitoring"] == True:
                return '{"status": "2", "message": "You are currently monitoring, you can only monitor ONE at a time"}'
            known_face_encondings = []
            known_face_names = []
            known_face_ids = []
            subject = get_pending_sched_id([request.form["id"], userdata["id"]])

            changeUserData(token, "showcam", True)
            ref = get_sect_ref([subject])
            dir = "./photos"
            for row in ref:
                known_face_encondings.append(
                    json.load(
                        open(
                            dir + "/" + row[2],
                        )
                    )
                )
                known_face_names.append(row[1])
                known_face_ids.append(row[0])
            saveJson(userdata["randS"] + "known_face_encondings", known_face_encondings, "json")
            saveJson(userdata["randS"] + "known_face_names", known_face_names, "json")
            saveJson(userdata["randS"] + "known_face_ids", known_face_ids, "json")

            start_time = utc.localize(datetime.now())
            # print(start_time)
            changeUserData(token, "monitoring", True)
            changeUserData(token, "monitor_sect", subject)
            changeUserData(token, "monitoring_type", 2)
            changeUserData(token, "monintor_late_time", str(start_time + timedelta(minutes=int(15))))
            changeUserData(token, "monitor_sched", request.form["id"])

            return '{"status": "1", "message": "Successfully Loaded Section References"}'
        elif link == "setmonitoring":
            if userdata["monitoring"] == True:
                return '{"status": "2", "message": "You are currently monitoring, you can only monitor ONE at a time"}'
            known_face_encondings = []
            known_face_names = []
            known_face_ids = []
            section = decrypt(request.form["section"], key)
            # userdata['showcam'] = (True if "showcam" in request.form  else False)
            changeUserData(token, "showcam", (True if "showcam" in request.form else False))
            ref = get_sect_ref([section])
            dir = "./photos"
            for row in ref:
                # known_face_encondings = json.load(open(row[2],))
                known_face_encondings.append(
                    json.load(
                        open(
                            dir + "/" + row[2],
                        )
                    )
                )
                known_face_names.append(row[1])
                known_face_ids.append(row[0])
                # encoded_image = fr.load_image_file(dir + "/" + row[2])
                # if (len(fr.face_encodings(encoded_image)) >= 1):
                #     face_encoding = fr.face_encodings(encoded_image)[0].tolist()
                #     known_face_encondings.append(face_encoding)
                #     known_face_names.append(row[1])

            saveJson(userdata["randS"] + "known_face_encondings", known_face_encondings, "json")
            saveJson(userdata["randS"] + "known_face_names", known_face_names, "json")
            saveJson(userdata["randS"] + "known_face_ids", known_face_ids, "json")

            start_time = utc.localize(datetime.now())
            # print(start_time)
            changeUserData(token, "monitoring", True)
            changeUserData(token, "monitor_sect", section)
            changeUserData(token, "monitoring_type", 1)
            changeUserData(
                token, "monintor_late_time", str(start_time + timedelta(minutes=int(request.form["latetime"])))
            )
            changeUserData(token, "monitor_sched", create_sched((section, start_time, userdata["id"])))

            # userdata['monitor_sect'] = section
            # userdata['monintor_late_time'] = start_time + timedelta(minutes=int(request.form['latetime']))
            # userdata['monitor_sched'] = create_sched( (section, start_time,userdata['id']))

            return '{"status": "1", "message": "Successfully Loaded Section References"}'
        elif link == "stop_monitoring":
            changeUserData(token, "monitoring", False)
            if userdata["monitoring_type"] == 2:
                update_monitoring_stat([userdata["monitor_sched"]])
            return '{"status": "1", "message": "Successfully Stopped Monitoring"}'

        # DEPARTMENT FUNCTION START

        elif link == "get_departments_details":
            return (
                '{"status": "1", "message": "Successfully Loaded Section Details", "data":'
                + json.dumps(get_departments_details([1]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "get_archived_departments_details":
            return (
                '{"status": "1", "message": "Successfully Loaded Section Details", "data":'
                + json.dumps(get_departments_details([0]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "edit_department":
            addChangeLog([userdata["id"], "Edited a department named " + request.form["name"]])
            return json.dumps(edit_department([request.form["name"], request.form["isActive"], userdata["edit_dept"]]))
        elif link == "add_department":
            addChangeLog([userdata["id"], "Added a department named " + request.form["name"]])
            return json.dumps(add_department([request.form["name"]]))
        elif link == "get_edit_department":
            tempReturn = get_department_details([request.form["s"]])
            if len(tempReturn) >= 1:
                changeUserData(token, "edit_dept", request.form["s"])
                return (
                    '{"status": "1", "message": "Successful", "data": ["'
                    + tempReturn[0][1]
                    + '","'
                    + str(tempReturn[0][2])
                    + '"]}'
                )
            else:
                return ErrorString

        # DEPARTMENT FUNCTION END

        # GET FOR DROP DOWN START

        elif link == "get_subject_management":
            tempReturn = []
            returnData = get_all_subj_management([])
            for idx, val in enumerate(returnData):
                tempReturn.append([encrypt(str(val[0]), key), val[0], val[1] + " - " + val[2] + " (" + val[3] + ")"])
            return json.dumps(tempReturn)
        elif link == "get_section":
            tempReturn = []
            returnData = get_all_sect([])
            for idx, val in enumerate(returnData):
                tempReturn.append([encrypt(str(val[0]), key), val[0], val[1]])
            return json.dumps(tempReturn)
        elif link == "get_subject":
            tempReturn = []
            returnData = get_all_subj([userdata["id"]])
            for idx, val in enumerate(returnData):
                tempReturn.append([encrypt(str(val[0]), key), val[0], val[1] + " - " + val[2] + " (" + val[3] + ")"])
            return json.dumps(tempReturn)
        elif link == "get_roles":
            tempReturn = []
            returnData = get_all_roles()
            for idx, val in enumerate(returnData):
                tempReturn.append([encrypt(str(val[0]), key), val[0], val[1]])
            return json.dumps(tempReturn)
        elif link == "get_schedules":
            section = decrypt(parse_qs(parsed_url.query)["sid"][0], key)
            tempReturn = []
            returnData = get_schedules([section])
            for idx, val in enumerate(returnData):
                tempReturn.append(
                    [encrypt(str(val[0]), key), val[0], parser.parse(str(val[1])).strftime("%b %d,%Y %H:%M %p")]
                )
            return json.dumps(tempReturn)
        elif link == "get_years":
            tempReturn = []
            returnData = get_all_year([])
            for idx, val in enumerate(returnData):
                tempReturn.append([encrypt(str(val[0]), key), val[0], val[1]])
            return json.dumps(tempReturn)
        # GET FOR DROP DOWN END

        # SECTIONS FUNCTION START
        elif link == "get_sections_details_t":
            return (
                '{"status": "1", "message": "Successfully Loaded Section Details", "data":'
                + json.dumps(get_sections_details_t([userdata["id"]]), cls=DecimalEncoder)
                + "}"
            )

        elif link == "edit_section":
            addChangeLog([userdata["id"], "Edited a section named " + request.form["name"]])
            return json.dumps(edit_section([request.form["name"], request.form["isActive"], userdata["edit_sect"]]))
        elif link == "get_sections_details":
            return (
                '{"status": "1", "message": "Successfully Loaded Section Details", "data":'
                + json.dumps(get_sections_details([1]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "get_archived_sections_details":
            return (
                '{"status": "1", "message": "Successfully Loaded Section Details", "data":'
                + json.dumps(get_sections_details([0]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "add_section":
            addChangeLog([userdata["id"], "Added a section named " + request.form["name"]])
            return json.dumps(add_section([request.form["name"]]))
        elif link == "get_edit_section":
            tempReturn = get_section_details([request.form["s"]])
            if len(tempReturn) >= 1:
                changeUserData(token, "edit_sect", tempReturn[0][0])
                return (
                    '{"status": "1", "message": "Successful", "data": ["'
                    + tempReturn[0][1]
                    + '","'
                    + str(tempReturn[0][2])
                    + '"]}'
                )
            else:
                return ErrorString
        elif link == "get_teachers":
            tempReturn = []
            returnData = get_teachers([])
            for idx, val in enumerate(returnData):
                tempReturn.append([encrypt(str(val[0]), key), val[0], val[1]])
            return json.dumps(tempReturn)
        elif link == "get_departments":
            tempReturn = []
            returnData = get_departments([])
            for idx, val in enumerate(returnData):
                tempReturn.append([encrypt(str(val[0]), key), val[0], val[1]])
            return json.dumps(tempReturn)

        # SECTIONS FUNCTION END

        # STUDENTS FUNCTION START
        elif link == "add_student":
            addChangeLog([userdata["id"], "Added a student named " + request.form["name"]])

            email = ""
            if "email" in request.form:
                if checkEmailValid(request.form["email"]):
                    email = request.form["email"]
            return json.dumps(add_student([request.form["name"], userdata["selected_section"], email]))
        elif link == "add_student_management":
            addChangeLog([userdata["id"], "Added a student named " + request.form["name"]])
            email = ""
            if "email" in request.form:
                if checkEmailValid(request.form["email"]):
                    email = request.form["email"]
            return json.dumps(
                add_student_management(
                    [
                        request.form["name"],
                        email,
                    ],
                    json.loads(request.form["subjects"]),
                    key,
                    request.form["studId"].strip(),
                )
            )
        elif link == "get_edit_student":
            tempReturn = get_student_details([request.form["s"], userdata["selected_section"]])

            if len(tempReturn) >= 1:
                changeUserData(token, "edit_stud", tempReturn[0][0])
                return (
                    '{"status": "1", "message": "Successful", "data": ["'
                    + tempReturn[0][1]
                    + '","'
                    + str(tempReturn[0][2])
                    + '","'
                    + str(tempReturn[0][3])
                    + '"]}'
                )
            else:
                return ErrorString
        elif link == "get_edit_student_rev":
            tempReturn = get_student_details_rev([request.form["s"]])

            if len(tempReturn) >= 1:
                changeUserData(token, "edit_stud", tempReturn[0][0])
                return (
                    '{"status": "1", "message": "Successful", "data": ["'
                    + tempReturn[0][1]
                    + '","'
                    + str(tempReturn[0][2])
                    + '","'
                    + str(tempReturn[0][3])
                    + '","'
                    + str(tempReturn[0][4])
                    + '","'
                    + str(tempReturn[0][5])
                    + '"]}'
                )
            else:
                return ErrorString
        elif link == "insert_image":
            input = request.form["imgBase64"].split(",")[1]
            img = ""
            # Convert Base64 Image to PIL to RGB
            img = toRGB(stringToImage(input))
            if len(fr.face_encodings(img)) == 0:
                return '{"status": "0", "message": "Invalid: No Face Detected"}'
            elif len(fr.face_encodings(img)) == 1:
                face_encoding = fr.face_encodings(img)[0].tolist()
                name = time.strftime("%Y%m%d_%H%M%S")
                saveJson(name, face_encoding, "photos")
                # face_encoding = fr.face_encodings(img)
                # face_location = fr.face_locations(img)
                # for (top, right, bottom, left), face_encoding in zip(face_location, face_encoding):

                #     # crop_img = img[top:top + (bottom-top), left:left + (right-left)]
                #     # img_name = time.strftime("%Y%m%d_%H%M%S") + '.png'
                #     # cv2.imwrite("./photos/" + img_name, img)
                #     name = time.strftime("%Y%m%d_%H%M%S")
                #     saveJson(name,face_encoding,'photos')

                # # Var_Class.capturedIMG += 1
                return '{"status": "1", "message":"Success: Photo Captured", "data": ["' + name + '.json"]}'
            else:
                return '{"status": "0", "message":"Invalid: More than one person"}'
            # cv2.imwrite("sample.jpg", img)
            return ""
        elif link == "delete_student_photos":
            p_names = delete_student_photos([userdata["edit_stud"]])
            for row in p_names:
                if os.path.isfile("./photos/" + row[0]):
                    os.remove("./photos/" + row[0])

            return '{"status": "1", "message":"Success: Deleted Photos"}'
        elif link == "edit_student":
            addChangeLog([userdata["id"], "Edited a student named " + request.form["name"]])
            # email = ""
            # if "email" in request.form:
            #     if checkEmailValid(request.form["email"]):
            #         email = request.form["email"]

            return json.dumps(
                edit_student(
                    [userdata["edit_stud"]],
                    json.loads(request.form["photo_names"]),
                )
            )
        elif link == "edit_student_management":
            addChangeLog([userdata["id"], "Edited a student named " + request.form["name"]])
            email = ""
            if "email" in request.form:
                if checkEmailValid(request.form["email"]):
                    email = request.form["email"]

            return json.dumps(
                edit_student_management(
                    [
                        request.form["name"],
                        email,
                        request.form["isValid"],
                        userdata["edit_stud"],
                    ],
                    json.loads(request.form["photo_names"]),
                    json.loads(request.form["subjects"]),
                    key,
                )
            )

        # STUDENTS FUNCTION END

        elif link == "manual_att":
            changeUserData(token, "monitor_sect", decrypt(request.form["sectionM"], key))
            changeUserData(token, "monitor_sched", decrypt(request.form["scheduleM"], key))
            return '{"status": "1", "message": "Loading you to Manual Attendance"}'
        elif link == "get_manual_att_listed":
            return (
                '{"status": "1", "message": "Successfully Loaded Section References", "data":'
                + json.dumps(
                    get_with_attendance([userdata["monitor_sched"], userdata["monitor_sect"]]), cls=DecimalEncoder
                )
                + "}"
            )
        elif link == "get_manual_att":
            return (
                '{"status": "1", "message": "Successfully Loaded Section References", "data":'
                + json.dumps(
                    get_no_attendance([userdata["monitor_sched"], userdata["monitor_sect"]]), cls=DecimalEncoder
                )
                + "}"
            )
        elif link == "set_manual_att":
            stat = request.form.getlist("stat")
            isValid = request.form.getlist("isValid")
            id = request.form.getlist("id")
            for idx, val in enumerate(id):
                current_time = utc.localize(datetime.now())
                value = (
                    userdata["monitor_sched"],
                    val,
                    current_time,
                    int(stat[idx]),
                    userdata["monitor_sect"],
                    1 if isValid[idx] == "1" else 0,
                )

                mark_stud(value)
            return '{"status": "1", "message": "Successfully Added Attendance"}'

        elif link == "get_stud_att_sum":
            tempReturn = []
            tempReturn.append(get_stud_att_sum([userdata["secttion_a_id"], userdata["id"], request.form["s"]]))
            # print(get_stud_att_sum([userdata['secttion_a_id'], request.form['s']]))
            tempReturn.append(get_headers([userdata["secttion_a_id"], userdata["id"]], 1))
            return json.dumps(tempReturn, cls=DecimalEncoder)
        elif link == "get_dashboard_details":
            tempReturn = []
            tempSection = []
            tempAbsent = []
            tempLate = []
            tempPresent = []
            tempExcused = []
            sections = get_all_subj([userdata["id"]])
            for idx, val in enumerate(sections):
                tempAtt = get_attendance([val[0], userdata["id"]], 1)

                tempSection.append(val[1] + " (" + val[2] + ")")
                tempAbsent.append(sum(x.count(0) for x in tempAtt))
                tempPresent.append(sum(x.count(1) for x in tempAtt))
                tempLate.append(sum(x.count(2) for x in tempAtt))
                tempExcused.append(sum(x.count(3) for x in tempAtt))

            tempReturn.append([tempSection, tempAbsent, tempPresent, tempLate, tempExcused])

            tempString = ""
            date_format = "%b %Y"
            cDate = datetime.today().strftime(date_format)
            dtObj = datetime.strptime(cDate, date_format)

            tempDate = []
            temp2Absent = []
            temp2Late = []
            temp2Present = []
            temp2Excused = []
            for x in range(6):
                tempAtt = get_attendance([str(dtObj.strftime("%Y")), str(dtObj.strftime("%m")), userdata["id"]], 2)

                temp2Absent.insert(0, sum(x.count(0) for x in tempAtt))
                temp2Present.insert(0, sum(x.count(1) for x in tempAtt))
                temp2Late.insert(0, sum(x.count(2) for x in tempAtt))
                temp2Excused.insert(0, sum(x.count(3) for x in tempAtt))

                # tempString += "     <br>Month"+str(dtObj.strftime('%m'))
                # tempString += "     <br>Year"+str(dtObj.strftime('%Y'))

                tempDate.insert(0, dtObj.strftime(date_format))
                dtObj = dtObj - relativedelta(months=1)

            tempReturn.append([tempDate, temp2Absent, temp2Present, temp2Late, temp2Excused])

            tempReturn.append(get_dashboard_det(userdata["id"]))

            return json.dumps(tempReturn, cls=DecimalEncoder)

        # ACCOUNT FUNCTIONS START

        # elif(link=="create_account"):

        #     # ty_id,ac_name,ac_email,ac_pass,ac_salt
        #     salt = ranStr(64)
        #     # cpass = ranStr(8)
        #     cpass = request.form['pass']
        #     spass = hash(salt,cpass)
        #     return json.dumps(add_account( [2, request.form['name'],request.form['email'],spass,salt]))
        elif link == "add_account":

            addChangeLog([userdata["id"], "Added an account named " + request.form["name"]])

            # ty_id,ac_name,ac_email,ac_pass,ac_salt
            salt = ranStr(64)
            # cpass = ranStr(8)
            cpass = ranStr(10)
            spass = hash(salt, cpass)
            dept_id = None
            if "deptA" in request.form:
                dept_id = decrypt(request.form["deptA"], key)

            # subject = "something testubg"
            # toEmail = "kristianamaba.kka@gmail.com"
            content = (
                "<table> <tbody> <tr> <td >Hi "
                + request.form["name"]
                + ",</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >The following is your account details for the AutoMoni System. </a></td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Name: "
                + request.form["name"]
                + "<br>Email: "
                + request.form["email"]
                + "<br>Password: "
                + cpass
                + "</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Thanks,</td> </tr> <tr> <td >The AutoMoni account admin.</td> </tr><tr> <td><br><br>DO NOT REPLY, THIS IS AN AUTOMATED MESSAGE</td> </tr> </tbody> </table>"
            )
            # toName = "Kristian Kurt"
            sendAsyncEmail("Account Created", request.form["name"], request.form["email"], content)

            return json.dumps(
                add_account(
                    [
                        decrypt(request.form["roles"], key),
                        request.form["name"],
                        request.form["email"],
                        spass,
                        salt,
                        dept_id,
                    ]
                )
            )
        elif link == "get_edit_account":
            tempReturn = get_account_details([request.form["s"]])
            if len(tempReturn) >= 1:
                changeUserData(token, "edit_ac", tempReturn[0])
                return (
                    '{"status": "1", "message": "Successful", "data": ["'
                    + tempReturn[1]
                    + '","'
                    + tempReturn[2]
                    + '","'
                    + str(tempReturn[3])
                    + '","'
                    + str(tempReturn[4])
                    + '","'
                    + str(tempReturn[5])
                    + '"]}'
                )
            else:
                return ErrorString
        elif link == "edit_account":
            addChangeLog([userdata["id"], "Edited an account named " + request.form["name"]])
            dept_id = None
            if "deptE" in request.form:
                dept_id = decrypt(request.form["deptE"], key)
            return json.dumps(
                edit_account(
                    [
                        request.form["name"],
                        request.form["email"],
                        dept_id,
                        decrypt(request.form["rolesE"], key),
                        request.form["isActive"],
                        userdata["edit_ac"],
                    ]
                )
            )

        # ACCOUNT FUNCTIONS END

        elif link == "change_pass":
            return json.dumps(
                change_pass(
                    [request.form["currentPW"], request.form["newPW"], request.form["repeatnewPW"], userdata["email"]]
                )
            )
        elif link == "get_attendance_sum":
            return (
                '{"status": "1", "message": "Successfully Loaded Attendance Summary", "section" : "'
                + userdata["att_sect_name"]
                + '", "data":'
                + json.dumps(get_attendance([userdata["secttion_a_id"], userdata["id"]], 1), cls=DecimalEncoder)
                + ', "header":'
                + json.dumps(get_headers([userdata["secttion_a_id"], userdata["id"]], 1), cls=DecimalEncoder)
                + "}"
            )
        elif link == "get_all_management_det":
            return (
                '{"status": "1", "message": "Successfully Students List", "data":'
                + json.dumps(get_all_students([1]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "get_archived_all_management_det":
            return (
                '{"status": "1", "message": "Successfully Students List", "data":'
                + json.dumps(get_all_students([0]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "get_management_det":
            return (
                '{"status": "1", "message": "Successfully Loaded Attendance Summary", "section" : "'
                + userdata["man_sect_name"]
                + '", "data":'
                + json.dumps(get_sect_students([userdata["selected_section"]]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "set_attendance":
            tempReturn = get_subject_details([request.form["s"]])
            changeUserData(token, "att_sect_name", tempReturn[0][1])
            changeUserData(token, "secttion_a_id", str(tempReturn[0][0]))
            # changeUserData(token, 'secttion_a_id',get_section_id( [request.form['s'],userdata['id']]))
            return '{"status": "1", "message": "Successfully Loaded"}'
        elif link == "set_management":
            sectDetails = get_sectid_byname([request.form["s"]])
            changeUserData(token, "man_sect_name", str(sectDetails[1]))
            changeUserData(token, "selected_section", str(sectDetails[0]))
            return '{"status": "1", "message": "Successfully Loaded"}'

        # SUBJECT FUNCTIONS START

        elif link == "get_subjects_details_t":
            return (
                '{"status": "1", "message": "Successfully Loaded Subject References", "data":'
                + json.dumps(get_subjects_details_t([userdata["id"]]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "get_subjects_details":
            return (
                '{"status": "1", "message": "Successfully Loaded Subject References", "data":'
                + json.dumps(get_subjects_details([1]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "get_archived_subjects_details":
            return (
                '{"status": "1", "message": "Successfully Loaded Subject References", "data":'
                + json.dumps(get_subjects_details([0]), cls=DecimalEncoder)
                + "}"
            )
        elif link == "add_subject":
            addChangeLog([userdata["id"], "Added a Subject named " + request.form["name"]])
            # ayear = ""

            # if "ayear" in request.form and request.form["ayear"] != "":
            #     ayear = request.form["ayear"]

            # else:
            #     ayear = str(datetime.now().year) + " - " + str(datetime.now().year + 1)
            return json.dumps(
                add_subject(
                    [
                        request.form["name"],
                        decrypt(request.form["deptA"], key),
                        decrypt(request.form["sectionA"], key),
                        decrypt(request.form["aayear"], key),
                        decrypt(request.form["teacherA"], key),
                    ]
                )
            )
        elif link == "get_edit_subject":
            tempReturn = get_subject_details([request.form["s"]])

            if len(tempReturn) >= 1:

                changeUserData(token, "edit_subject", tempReturn[0][0])
                return (
                    '{"status": "1", "message": "Successful", "data": ["'
                    + str(tempReturn[0][0])
                    + '","'
                    + str(tempReturn[0][1])
                    + '","'
                    + str(tempReturn[0][2])
                    + '","'
                    + str(tempReturn[0][3])
                    + '","'
                    + str(tempReturn[0][4])
                    + '","'
                    + str(tempReturn[0][5])
                    + '","'
                    + str(tempReturn[0][6])
                    + '"]}'
                )
            else:
                return ErrorString
        elif link == "edit_subject":
            addChangeLog([userdata["id"], "Edited a Subject named " + request.form["name"]])
            # ayear = ""
            # if "ayear" in request.form and request.form["ayear"] != "":
            #     ayear = request.form["ayear"]
            # else:
            #     ayear = str(datetime.now().year) + " - " + str(datetime.now().year + 1)
            return json.dumps(
                edit_subject(
                    [
                        request.form["name"],
                        decrypt(request.form["deptE"], key),
                        decrypt(request.form["sectionE"], key),
                        decrypt(request.form["ayear"], key),
                        decrypt(request.form["teacherE"], key),
                        request.form["isActive"],
                        userdata["edit_subject"],
                    ]
                )
            )

        # SUBJECT FUNCTIONS END

        elif link == "getUserData":
            curl = parsed_url.scheme + "://" + parsed_url.netloc + "/monitoring/"
            returnTemp = getUserDataLive(token)
            if len(returnTemp) >= 1:
                return (
                    '{"status": "1", "message": "Successful", "data": '
                    + json.dumps(returnTemp)
                    + ', "enc": "'
                    + curl
                    + str(token)
                    + '"}'
                )
            else:
                return '{"status": "2", "message": "Invalid Link", "enc": "' + curl + str(token) + '"}'
        elif link == "get_accounts_details":
            return (
                '{"status": "1", "message": "Successfully Loaded Account Details", "data":'
                + json.dumps(get_accounts_details(1), cls=DecimalEncoder)
                + "}"
            )
        elif link == "get_archived_accounts_details":
            return (
                '{"status": "1", "message": "Successfully Loaded Account Details", "data":'
                + json.dumps(get_accounts_details(0), cls=DecimalEncoder)
                + "}"
            )

        elif link == "get_changelogs":
            return (
                '{"status": "1", "message": "Successfully Loaded Logs", "data":'
                + json.dumps(get_changelogs(), cls=DecimalEncoder, default=str)
                + "}"
            )
        elif link == "get_loginlogs":
            return (
                '{"status": "1", "message": "Successfully Loaded Logs", "data":'
                + json.dumps(get_loginlogs(), cls=DecimalEncoder, default=str)
                + "}"
            )
            # get_changelogs

        elif link == "get_adv_set":
            return (
                '{"status": "1", "message": "Successfully Loaded Settings", "data":'
                + json.dumps(get_adv_set(), cls=DecimalEncoder, default=str)
                + "}"
            )
        elif link == "edit_adv_set":
            addChangeLog([userdata["id"], "Edited the Advanced Settings"])
            return json.dumps(
                edit_adv_set(
                    [request.form["absent_num"], request.form["late_num"], decrypt(request.form["ayear"], key)]
                )
            )

        else:
            return ErrorString
    except NameError:
        return ErrorString


@app.route("/cron/<link>", methods=["POST", "GET"])
@cross_origin()
def cron_job(link):
    if link == "cronjob":
        max_absent = int(get_adv_set()[0][1])
        subjects = get_subjects_details([1])
        temptext = ""

        for idx, val in enumerate(subjects):
            tempAtt = get_attendance([val[0], val[6]], 1)

            students = ""
            for idx2, val2 in enumerate(tempAtt):
                absences = countElement(val2[2:], 0)

                # checkNotif(value):addNotif(value):
                percent = absences / max_absent
                percent = 100 if percent > 1 else round(percent * 100)

                prog_stat = "over the limit" if percent == 100 else ("warning" if percent >= 50 else "safe")

                if percent == 100 and checkNotif([val2[0], absences]):
                    email = get_student_email([val2[0], val[7]])
                    temptext += val2[1] + " (" + str(absences) + ") is " + prog_stat + " (" + email + ")<br>"
                    if checkEmailValid(email):
                        # send to email
                        addNotif([val2[0], absences])
                        students += "{} with {} Absences <br>".format(val2[1], str(absences))
                        content = (
                            "<table> <tbody> <tr> <td >Hi "
                            + val2[1]
                            + ",</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Your absences is over the threshold, please contact your professor for details or clarifications. </a></td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Subject: "
                            + val[1]
                            + "<br>Total Absences: "
                            + str(absences)
                            + "<br>Absent Threshold: "
                            + str(max_absent)
                            + "</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Thanks,</td> </tr> <tr> <td >The AutoMoni account admin.</td> </tr><tr> <td><br><br>DO NOT REPLY, THIS IS AN AUTOMATED MESSAGE</td> </tr> </tbody> </table>"
                        )
                        # print(content)
                        # toName = "Kristian Kurt"
                        sendAsyncEmail("Your Absences is " + prog_stat, val2[1], email, content)

                        # print("send email")
            if students != "":
                content = (
                    "<table> <tbody> <tr> <td >Hi "
                    + val[3]
                    + ",</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Your class have student/s that exceeded the max absent threshhold. </a></td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Subject: "
                    + val[1]
                    + "<br>Student/s: <br><br>"
                    + students
                    + "</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Thanks,</td> </tr> <tr> <td >The AutoMoni account admin.</td> </tr><tr> <td><br><br>DO NOT REPLY, THIS IS AN AUTOMATED MESSAGE</td> </tr> </tbody> </table>"
                )
                # print(content)
                # toName = "Kristian Kurt"
                sendAsyncEmail("Subject Exceeding Absences ", val[3], val[8], content)

        # tempReturn.append([tempSection,tempAbsent,tempPresent,tempLate,tempExcused])
        return temptext + "Cron Done"
    return "Invalid Key"

    # projectpath = request.form['projectFilepath']


def countElement(arr, element):
    count = 0
    for idx, val in enumerate(arr):
        if element == val:
            count += 1
    return count


@socketio.on("live-list-check", namespace="/live")
def live_list(value, type, stage):
    # parsed_url = urlparse(request.url)
    # token = None
    # userdata = None
    # if("s" in parse_qs(parsed_url.query)):
    #     token = parse_qs(parsed_url.query)['s'][0]
    #     userdata = getUserData(token)
    try:
        if type == 1 and stage == 1:
            emit("live-list-out", get_marked_attendance(value), namespace="/live")
        if type == 1 and stage == 2:
            emit("live-list-out", get_verified_attendance(value), namespace="/live")
        elif type == 2:
            emit("live-list-out", session["live-list"], namespace="/live")
            session["live-list"] = []
    except Exception as exc:
        print(exc)

    # changeUserData(token, 'live_list', json.dumps([]))


@socketio.on("input image", namespace="/live")
def test_message(input, userdata, type, stage):
    # print(some['some'])
    try:
        # parsed_url = urlparse(request.url)
        # parsed_url = urlparse(request.url)
        # token = None
        # userdata = None
        # livelist = None
        # if("s" in parse_qs(parsed_url.query)):
        #     token = parse_qs(parsed_url.query)['s'][0]
        #     userdata = getUserData(token)
        #     livelist = json.loads(userdata['live_list'])

        # session['live-list'] = []
        # changeUserData(token, 'live-list',[])

        input = input.split(",")[1]
        img = ""
        # Convert Base64 Image to PIL to RGB
        img = toRGB(stringToImage(input))
        del input
        # cv2.imwrite("sample.jpg", img)

        # Get RGB Image Descriptions
        height, width, _ = img.shape

        # Convert RGB image to Blob
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

        # Opening JSON file
        known_face_encondings = json.load(
            open(
                "./json/" + userdata[0] + "known_face_encondings.json",
            )
        )
        known_face_names = json.load(
            open(
                "./json/" + userdata[0] + "known_face_names.json",
            )
        )
        known_face_ids = json.load(
            open(
                "./json/" + userdata[0] + "known_face_ids.json",
            )
        )

        # face_locations = fr.face_locations(img)
        # face_encodings = fr.face_encodings(img, face_locations)

        # for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        #     matches = fr.compare_faces(known_face_encondings, face_encoding)

        #     name = "Unknown"

        #     face_distances = fr.face_distance(known_face_encondings, face_encoding)

        #     best_match_index = np.argmin(face_distances)
        #     if matches[best_match_index]:
        #         stud_id = known_face_ids[best_match_index]

        #         # START ATTENDANCE AREA

        #         current_time =  parser.parse(str(utc.localize(datetime.now())))

        #         monintor_late_time = parser.parse(userdata[1])
        #         name = known_face_names[best_match_index]
        #         if check_stud( (userdata[2], stud_id)) == 0:
        #             value = (userdata[2], stud_id, str(current_time)[:-13], ("1" if current_time < monintor_late_time else "2"),userdata[3])
        #             mark_stud(value)

        #             if(type==2):
        #                 session['live-list'].append([name, current_time.strftime('%b %d,%Y %H:%M %p'), ("1" if current_time < monintor_late_time else "2")])

        #         # END ATTENDANCE  AREA

        #     # changeUserData(token, 'live_list',json.dumps(livelist))
        #     cv2.rectangle(img, (left, top), (right, bottom), (0,255,0), 2)
        #     cv2.putText(img, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, .6, (0,255,0), 2)

        # Set Input Image to Algorithm
        net.setInput(blob)
        del blob
        scores = None
        class_id = None
        confidence = None
        center_x = None
        center_y = None
        w = None
        h = None
        x = None
        y = None
        crop_img = None
        tempEncode = None
        face_encoding = None

        matches = None
        name = None
        face_distances = None
        best_match_index = None
        stud_id = None
        current_time = None
        monintor_late_time = None
        value = None
        layerOutputs = net.forward(output_layers_names)
        # Scan Results
        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Filter Results
                if confidence > 0.3 and class_id == 0:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    crop_img = img[y - 30 : y + h + 30, x - 30 : x + w + 30]

                    tempEncode = fr.face_encodings(crop_img)
                    # cv2.imwrite("sample.jpg", crop_img)
                    if len(tempEncode) >= 1:
                        face_encoding = tempEncode[0]

                        matches = fr.compare_faces(known_face_encondings, face_encoding)

                        name = "Unknown"

                        face_distances = fr.face_distance(known_face_encondings, face_encoding)

                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            stud_id = known_face_ids[best_match_index]

                            # print(stud_id)

                            # START ATTENDANCE AREA

                            current_time = parser.parse(str(utc.localize(datetime.now())))

                            monintor_late_time = parser.parse(userdata[1])
                            name = known_face_names[best_match_index]
                            # name = get_stud_name( [stud_id,userdata[3]])
                            if stage == 1:
                                if check_stud((userdata[2], stud_id), 1) == 0:
                                    value = (
                                        userdata[2],
                                        stud_id,
                                        str(current_time)[:-13],
                                        ("1" if current_time < monintor_late_time else "2"),
                                        userdata[3],
                                        0,
                                    )
                                    # mark_stud(value)

                                    threading.Thread(target=mark_stud, args=([value])).start()

                                    if type == 2:
                                        session["live-list"].append(
                                            [
                                                name,
                                                current_time.strftime("%b %d,%Y %H:%M %p"),
                                                ("1" if current_time < monintor_late_time else "2"),
                                            ]
                                        )
                            else:
                                att_id = check_stud((userdata[2], stud_id), 2)
                                if att_id >= 1:
                                    threading.Thread(target=validate_att, args=([[att_id]])).start()
                                    if type == 2:
                                        session["live-list"].append(
                                            [
                                                name,
                                                current_time.strftime("%b %d,%Y %H:%M %p"),
                                                "1",
                                            ]
                                        )

                        # END ATTENDANCE  AREA
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(img, name, (x + 6, y + h - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        del known_face_encondings, known_face_names, known_face_ids

        del (
            scores,
            class_id,
            confidence,
            center_x,
            center_y,
            w,
            h,
            x,
            y,
            crop_img,
            tempEncode,
            face_encoding,
            matches,
            name,
        )
        del face_distances, best_match_index, stud_id, current_time, monintor_late_time, value

        retval, buffer_img = cv2.imencode(".jpg", img)
        image_data = base64.b64encode(buffer_img).decode("utf-8")  # Do your magical Image processing here!!
        gc.collect()
        # image_data = image_data.decode("utf-8")
        if userdata[4]:
            image_data = "data:image/jpeg;base64," + image_data
            # print("OUTPUT " + image_data)
            emit("out-image-event", {"image_data": image_data, "enable": "1"}, namespace="/live")
        else:
            emit("out-image-event", {"enable": "0"}, namespace="/live")

    except Exception as exc:
        gc.collect()
        print(exc)


@socketio.on("connect", namespace="/live")
def test_connect():
    app.logger.info("client connected")


# def gen():
#     """Video streaming generator function."""

#     app.logger.info("starting to generate frames!")
#     while True:
#         frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/video_feed')
# def video_feed():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    socketio.run(app)

if __name__ == "__main__":
    app.run(ssl_context="adhoc", threaded=True)
