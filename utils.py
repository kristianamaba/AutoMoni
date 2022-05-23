import base64
import codecs
import decimal
import io
import json
import os.path
import re
import threading
from datetime import date, datetime, timedelta
from hashlib import sha256
from random import choice
from string import ascii_uppercase

import cv2
import numpy as np
import pytz
import requests
from cryptography.fernet import Fernet
from dateutil import parser
from flask import Flask, session
from PIL import Image

utc = pytz.UTC


def sendAsyncEmail(subject, toName, toEmail, content):
    threading.Thread(target=sendEmail, args=(subject, toName, toEmail, content)).start()


email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
key2 = Fernet.generate_key()  # this is your "password"
cipher_suite = Fernet(key2)


def sendEmail(subject, toName, toEmail, content):
    # subject = "something testubg"
    # toEmail = "kristianamaba.kka@gmail.com"
    # content = "<table> <tbody> <tr> <td >Hi {$name},</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >The following is your account details for the Meg & Jane studio Transaction System. </a></td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Name: {$name}<br>Email: {$email}<br>Password: {$genPass}</td> </tr> <tr> <td >&nbsp;</td> </tr> <tr> <td >Thanks,</td> </tr> <tr> <td >The Meg & Jane studio account admin.</td> </tr> </tbody> </table>"

    query = {
        "subject": subject,
        "fromName": "AutoMoni System",
        "toName": "AutoMoni User:" + toName,
        "toEmail": toEmail,
        "content": content,
    }
    requests.post("http://localhost/c/index.php/Main_controller/sendEmailPost", data=query)


def checkEmailValid(email):

    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(email_regex, email):
        return True
    else:
        return False


def getDateTime():
    current_time = parser.parse(str(utc.localize(datetime.now())))
    return str(current_time)[:-13]


# def getUserData(s):
#     userdata = json.load(open('./userdata/'+s+'.json',))
#     return userdata

# def changeUserData(s, ref, string):
#     userdata = json.load(open('./userdata/'+s+'.json',))
#     userdata[ref] = string
#     saveJson(s,userdata,"userdata")

# def createUserData(name):
#     arr = {
#         "id": None,
#         "ty": None,
#         "name": None,
#         "email": None,
#         "randS": name,
#         "showcam": None,
#         "monitor_sect": None,
#         "monintor_late_time": None,
#         "monitor_sched": None,
#         "edit_sect": None,
#         "edit_subject": None,
#         "edit_stud": None,
#         "att_sect_name": None,
#         "secttion_a_id": None,
#         "man_sect_name": None,
#         "selected_section": None,
#         "live-list": []
#     }
#     saveJson(name,arr,"userdata")


def ranStr(n):
    return "".join(choice(ascii_uppercase) for i in range(n))


def hash(s, d):
    return sha256((s + d).encode("utf")).hexdigest()


def saveJson(name, dictionary, loc):
    if os.path.isfile("./" + loc + "/" + name + ".json"):
        os.remove("./" + loc + "/" + name + ".json")
    else:
        open("./" + loc + "/" + name + ".json", "x")

    ### this saves the array in .json format
    json.dump(
        dictionary,
        codecs.open("./" + loc + "/" + name + ".json", "w", encoding="utf-8"),
        separators=(",", ":"),
        sort_keys=True,
        indent=4,
    )


# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))


# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890123456789abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"


def encrypt(message, key):
    return str(cipher_suite.encrypt(message.encode("utf-8")))[2:-1]
    # encrypted = ''
    # for chars in message:
    #     if chars in LETTERS:
    #         num = LETTERS.find(chars)
    #         num += key
    #         encrypted +=  LETTERS[num]

    # return encrypted


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def decrypt(message, key):
    return cipher_suite.decrypt(message.encode("utf-8")).decode("utf-8")
    # decrypted = ''
    # for chars in message:
    #     if chars in LETTERS:
    #         num = LETTERS.find(chars)
    #         num -= key
    #         decrypted +=  LETTERS[num]

    # return decrypted


# <img src="./assets/images/users/unnamed.png" alt="user" class="rounded-circle" width="40">
def profileDropdown():
    return (
        """ <ul class="navbar-nav float-right">
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="javascript:void(0)" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            
            <span class="fa fa-user-circle" class="rounded-circle" width="40" ></span>
            <span class="ml-2 d-none d-lg-inline-block"><span class="text-dark">"""
        + session["name"]
        + """</span> <i data-feather="chevron-down" class="svg-icon"></i></span>
        </a>
        <div class="dropdown-menu dropdown-menu-right user-dd animated flipInY">
            <a class="dropdown-item" href="javascript:$('#main-wrapper').attr('data-sidebartype', ($('#main-wrapper').attr('data-sidebartype') == 'full' ? 'mini-sidebar' : 'full')).attr('class', ($('#main-wrapper').attr('data-sidebartype') == 'full' ? 'mini-sidebar' : 'full')); setTimeout(function(){ $($.fn.dataTable.tables(true)).DataTable().columns.adjust(); }, 500);"><i class="fas fa-wrench mr-3"></i>Toggle Mini-Sidebar</a>
            <a class="dropdown-item" href="/settings"><i data-feather="settings" class="svg-icon mr-2 ml-1"></i>
                Settings</a>
            <a class="dropdown-item" href="/logout"><i data-feather="power" class="svg-icon mr-2 ml-1"></i>
                Logout</a>
        </div>
    </li>
</ul>"""
    )


def menubar():
    menu = """<aside class="left-sidebar" data-sidebarbg="skin6">
    <!-- Sidebar scroll-->
    <div class="scroll-sidebar" data-sidebarbg="skin6">
        <!-- Sidebar navigation-->
        <nav class="sidebar-nav">
            <ul id="sidebarnav">"""

    # Menu = [["Dashboard","dashboard","home"],
    #         ["Monitoring","monitoring","monitor"],
    #         ["Sections","sections","book-open"],
    #         ["Accounts","accounts","users"]
    #         ];

    #         #

    # permission= {1 : [0,1,2,3],
    #             2 : [0,2],
    #             3 : []};

    # # Loop Menu Options based on Login Menu Access

    # for key in permission[1]:
    #     if(session['linkTabs'] == Menu[key][1]):
    #         # menu += '<li class="sidebar-item selected"> <a class="sidebar-link sidebar-link active" href="./' . $menu->Href . '" aria-expanded="false"><i class="fas fa-' . $menu->Icon . '"></i><span class="hide-menu">' . $menu->Name . '</span></a></li>';
    #         menu += '<li class="sidebar-item selected"> <a class="sidebar-link sidebar-link active" href="' + Menu[key][1] + '" aria-expanded="false"><i data-feather="' + Menu[key][2] + '" class="feather-icon"></i><span class="hide-menu">' + Menu[key][0] + '</span></a></li>'
    #     else:
    #         menu += '<li class="sidebar-item"> <a class="sidebar-link sidebar-link" href="' + Menu[key][1] + '" aria-expanded="false"><i data-feather="' + Menu[key][2] + '" class="feather-icon"></i><span class="hide-menu">' + Menu[key][0] + '</span></a></li>'

    for row in session["menu"]:
        # m.Name, m.Href, m.Icon
        if session["linkTabs"] == row[1]:
            menu += (
                '<li class="sidebar-item selected"> <a class="sidebar-link sidebar-link active" href="/'
                + row[1]
                + '" aria-expanded="false"><i data-feather="'
                + row[2]
                + '" class="feather-icon"></i><span class="hide-menu">'
                + row[0]
                + "</span></a></li>"
            )
        else:
            menu += (
                '<li class="sidebar-item"> <a class="sidebar-link sidebar-link" href="/'
                + row[1]
                + '" aria-expanded="false"><i data-feather="'
                + row[2]
                + '" class="feather-icon"></i><span class="hide-menu">'
                + row[0]
                + "</span></a></li>"
            )

    menu += """</ul>
                </nav>
                <!-- End Sidebar navigation -->
            </div>
            <!-- End Sidebar scroll-->
        </aside>"""
    return menu
