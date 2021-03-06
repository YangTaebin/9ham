from flask import Flask, render_template, request, json
import pymysql
import hashlib
import base64
import random
import smtplib
from email.mime.text import MIMEText
import os.path

app = Flask(__name__)

def ban_username(username):
    ban_char=["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    for i in ban_char:
        if i in username:
            return True
    return False

def email_from_username(username):
    c_username = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    username_cursor = c_username.cursor(pymysql.cursors.DictCursor)
    sql = "select email from user_info where username='"+str(username)+"';"
    username_cursor.execute(sql)
    result = username_cursor.fetchall()[0]["email"]
    return result

def email_check(email):
    ban_list = ["sharklasers.com", "guerrillamail.info", "grr.la", "guerrillamail.biz", "guerrillamail.com", "guerrillamail.org", "guerrillamail.net", "guerrillamail.de", "guerrillamailblock.com", "pokemail.net", "spam4.me", "nicoric.com", "givmail.com", "rffff.net", "mytrashmailer.com", "ruu.kr", "ovooovo.com"]
    count = 0
    for i in email:
        if i == "@":
            count+= 1
    if count != 1:
        return False
    count = 0
    for j in email.split("@")[1]:
        if j == ".":
            count += 1
    if count > 2:
        return False

    if email.split("@")[1] in ban_list:
        return False

    return True


def username_check(username):
    c_username = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    username_cursor = c_username.cursor(pymysql.cursors.DictCursor)
    sql = "select exists (select username from user_info where username='"+str(username)+"') as exi;"
    username_cursor.execute(sql)
    exi = username_cursor.fetchall()[0]["exi"]
    return exi == 1

def exist_email(email):
    e_check = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    e_check_cursor = e_check.cursor(pymysql.cursors.DictCursor)

    sql = "select exists (select email from user_info where email='"+str(email)+"') as exi;"
    e_check_cursor.execute(sql)
    exists = e_check_cursor.fetchall()[0]["exi"]
    if exists == 1:
        return True
    return False

def exist_checker(checker):
    checker_check = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    checker_check_cursor = checker_check.cursor(pymysql.cursors.DictCursor)
    sql = "select exists (select email_check from user_info where email_check='"+str(checker)+"') as exi"
    checker_check_cursor.execute(sql)
    exists = checker_check_cursor.fetchall()[0]["exi"]
    if exists == 1:
        return True
    return False

def check_checker(email, checker):
    checker_check = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    checker_check_cursor = checker_check.cursor(pymysql.cursors.DictCursor)
    sql = "select email_check from user_info where email='"+str(email)+"';"
    checker_check_cursor.execute(sql)
    db_checker = checker_check_cursor.fetchall()[0]["email_check"]
    return(db_checker == checker)

def get_tag_username(username):
    checker = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    checker_cursor = checker.cursor(pymysql.cursors.DictCursor)
    sql = "select email_check from user_info where username='"+str(username)+"';"
    checker_cursor.execute(sql)
    check_code = str(checker_cursor.fetchall()[0]["email_check"])
    tag = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_user_tags")
    tag_cursor = tag.cursor(pymysql.cursors.DictCursor)
    sql="select tags from user_tags where checker='"+str(check_code)+"';"
    tag_cursor.execute(sql)
    tags = str(tag_cursor.fetchall()[0]["tags"])
    tags = tags.split(";;")
    return tags

def getchecker_username(username):
    checker = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    checker_cursor = checker.cursor(pymysql.cursors.DictCursor)
    sql = "select email_check from user_info where username='" + str(username) + "';"
    checker_cursor.execute(sql)
    check_code = str(checker_cursor.fetchall()[0]["email_check"])
    return check_code

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/login")
def login():
    return render_template("login.html", error=0, cookie="null", username="null")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/change_profile")
def change_profile():
    return render_template("change_profile.html", error=5)

@app.route("/change_profile", methods=["POST"])
def change_profile_submit():
    username = request.form["profile_username"]
    passwd = request.form["profile_passwd"]
    age = request.form["profile_age"]
    affi = request.form["profile_affi"]
    lane = request.form["profile_lane"]
    email = request.form["profile_email"]
    ham = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    ham_cursor = ham.cursor(pymysql.cursors.DictCursor)
    sql = "select exists (select * from user_info where username='"+username+"') as success;"
    ham_cursor.execute(sql)
    exists = ham_cursor.fetchall()[0]["success"]
    if exists != 1:
        return render_template("change_profile.html", error=1)

    sql="select * from user_info where username='"+str(username)+"';"
    ham_cursor.execute(sql)
    user_data = ham_cursor.fetchall()[0]

    N = 2
    for i in range(N):
        passwd = hashlib.sha256(passwd.encode()).hexdigest()

    if passwd != user_data["password"]:
        return render_template("change_profile.html", error=2)
    if email != user_data["email"]:
        return render_template("change_profile.html", error=3)

    sql = "update user_info set age="+str(age)+", affi='"+str(affi)+"' where username='"+str(username)+"';"
    ham_cursor.execute(sql)
    ham.commit()
    return render_template("change_profile.html", error=0)

@app.route("/tag_change")
def tag_change():
    return render_template("tag_change.html", error=5)

@app.route("/tag_change", methods=["POST"])
def tag_change_submit():
    username = request.form["profile_username"]
    passwd = request.form["profile_passwd"]
    tags = []
    num = 0
    while True:
        if "select_"+str(num)+"_tags" in request.form.keys():
            tags.append(request.form["select_"+str(num)+"_tags"])
        else: break
        num += 1
    real_tags = []
    for i in tags:
        if i not in real_tags:
            real_tags.append(i)
    tags = real_tags
    if len(tags) > 10:
        return render_template("tag_change.html", error=1)
    tags = ";;".join(tags)
    print(tags)
    ham = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    ham_cursor = ham.cursor(pymysql.cursors.DictCursor)
    sql = "select password from user_info where username='"+str(username)+"';"
    ham_cursor.execute(sql)
    passcode = ham_cursor.fetchall()[0]["password"]
    N = 2
    for i in range(N):
        passwd = hashlib.sha256(passwd.encode()).hexdigest()
    if passwd != passcode:
        return render_template("tag_change.html", error=2)

    sql = "select email_check from user_info where username='"+str(username)+"';"
    ham_cursor.execute(sql)
    checker = ham_cursor.fetchall()[0]["email_check"]

    hem = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_user_tags")
    hem_cursor = hem.cursor(pymysql.cursors.DictCursor)
    sql = "update user_tags set tags='"+str(tags)+"' where checker='"+str(checker)+"';"
    hem_cursor.execute(sql)
    hem.commit()

    return render_template("tag_change.html", error=0)

@app.route("/login", methods=["POST"])
def login_process():
    username = request.form['username']
    password = request.form['password']
    inpu = password
    N = 2

    for i in range(N):
        inpu = hashlib.sha256(inpu.encode()).hexdigest()
    input_passcode = inpu
    passcode = ""
    error = 0
    login = pymysql.connect(user="root", password="@dkfldkfl2021@", database="9ham_login", host="localhost")
    login_cursor = login.cursor(pymysql.cursors.DictCursor)

    sql = "select exists (select username from user_info where username='"+str(username)+"') as success;"
    login_cursor.execute(sql)
    success = login_cursor.fetchall()[0]["success"]
    if success != 1:
        error=1
        return render_template("login.html", error=error, cookie="null", username="null")

    email = email_from_username(username)

    for i in range(N):
        email = hashlib.sha256(email.encode()).hexdigest()
    cookie_passcode = email

    sql = "select password from user_info where username='"+str(username)+"';"
    login_cursor.execute(sql)
    login_result = login_cursor.fetchall()

    if len(login_result) == 1:
        passcode = login_result[0]["password"]
    if passcode != input_passcode:
        error=2
        return render_template("login.html", error=error, cookie="null", username="null")

    str1 = str(ord(cookie_passcode[0]))
    for i in cookie_passcode[1:]:
        str1 += ", "+str(ord(i))

    str2 = str(ord(username[0]))
    for i in username[1:]:
        str2 += ", " + str(ord(i))

    error=3
    return render_template("login.html", error=error, cookie=str1, username=str2)

@app.route("/registration")
def regist():
    return render_template("regist.html")

@app.route("/registration", methods=["POST"])
def regist_post_data():
    if not request.form["profile_img"]:
        error = 2
        return render_template("regist.html", error=error)
    if not request.form["username"]:
        error = 2
        return render_template("regist.html", error=error)
    if not request.form["password"]:
        error = 2
        return render_template("regist.html", error=error)
    if not request.form["email"]:
        error = 2
        return render_template("regist.html", error=error)

    profile_img = str(request.form["profile_img"])
    profile_img_filename = str(request.form["profile_img_filename"])
    username = str(request.form["username"])
    password = str(request.form["password"])
    email = str(request.form["email"])
    lane = str(request.form["select_lane"])

    if lane == "idea":
        lane = 0
    elif lane == "design":
        lane = 1
    elif lane == "develop":
        lane = 2

    age = "0"
    affi = ""

    if request.form["age"]:
        age = str(request.form["age"])

    if request.form["affi"]:
        affi = str(request.form["affi"])

    if not email_check(email):
        error = 4
        return render_template("regist.html", error=error)

    if not exist_email(email):
        error = 1
        return render_template("regist.html", error=error)

    error=0

    db_user_info = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    db_user_info_cursor = db_user_info.cursor(pymysql.cursors.DictCursor)

    sql = "select exists (select * from user_info where username='"+str(username)+"') as success;"
    db_user_info_cursor.execute(sql)
    exist_id = db_user_info_cursor.fetchall()[0]["success"]

    if exist_id == 1:
        error = 3
        return render_template("regist.html", error=error)

    password = hashlib.sha256(password.encode()).hexdigest()
    password = hashlib.sha256(password.encode()).hexdigest()

    if profile_img_filename.split(".")[1] == "jpg":
        filename = "static/profile_img/profile_"+username+".jpg"
    elif profile_img_filename.split(".")[1] == "png":
        filename = "static/profile_img/profile_" + username + ".png"
    else:
        error = 5
        return render_template("regist.html", error=error)
    imgdata = base64.b64decode(profile_img)
    with open(filename, 'wb') as f:
        f.write(imgdata)

    db_user_info = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    db_user_info_cursor = db_user_info.cursor(pymysql.cursors.DictCursor)

    sql = "update user_info set username='"+str(username)+"', password='"+str(password)+"', lane="+str(lane)+", age="+str(age)+", affi='"+str(affi)+"' where email='"+str(email)+"';"
    db_user_info_cursor.execute(sql)
    db_user_info.commit()

    checker = getchecker_username(username)

    tags = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_user_tags")
    tags_cursor = tags.cursor(pymysql.cursors.DictCursor)

    sql = "insert into user_tags (checker, tags) values ('"+str(checker)+"','')"
    tags_cursor.execute(sql)
    tags.commit()

    return render_template("regist.html", error=error)

@app.route("/already_username", methods=["POST"])
def already_username():
    username = request.get_json()["username"]
    if ban_username(username):
        return json.dumps({"exist": 2})
    if username_check(username):
        return json.dumps({"exist": 1})
    return json.dumps({"exist": 0})

@app.route("/email_check",methods=["POST"])
def email_auth():
    email_data = request.get_json()["Email"]
    if not email_check(email_data):
        return json.dumps({"status": "failed", "error": 1})

    if exist_email(email_data):
        return json.dumps({"status": "failed", "error": 2})

    while True:
        email_checker = random.randint(0, 999999)
        email_checker = str(email_checker).zfill(6)
        checker = email_checker
        email_checker = hashlib.sha256(email_checker.encode()).hexdigest()
        if not exist_checker(email_checker):
            break

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login("9hamofficial@gmail.com", "cxnyfeizoiascqpi")
    msg = MIMEText("??????????????????\n?????? ???????????? ?????? ???????????? ?????? ????????? ?????????????????????.\n???????????? ?????? ?????? ??????????????? ??????????????????.\n\n" + str(
        checker) + "\n\n?????? 9ham ???????????? ?????????????????? ???????????????.")
    msg["Subject"] = "9ham ???????????? ????????? ?????????"
    msg["To"] = email_data
    smtp.sendmail("9hamofficial@gmail.com", email_data, msg.as_string())
    smtp.quit()

    regist_email = pymysql.connect(user="root", password="@dkfldkfl2021@", database="9ham_login")
    regist_email_cursor = regist_email.cursor(pymysql.cursors.DictCursor)
    sql = "insert into user_info (email, email_check) values ('"+str(email_data)+"', '"+str(email_checker)+"');"
    regist_email_cursor.execute(sql)
    regist_email.commit()

    return json.dumps({"status": "success", "error": 0})

@app.route("/checker_check", methods=["POST"])
def checker_check():
    checker = request.get_json()
    email = checker["email"]
    if not checker["checker"]:
        return json.dumps({"status": "failed", "error": 3})
    checker = hashlib.sha256(checker["checker"].zfill(6).encode()).hexdigest()
    if not exist_email(email):
        return json.dumps({"status": "failed", "error": 1})
    if not check_checker(email, checker):
        return json.dumps({"status": "failed", "error": 2})
    return json.dumps({"status": "success", "error": 0})

@app.route("/auth_username", methods=["POST"])
def auth_username():
    auth = request.get_json()["auth"]
    db_user_info = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    db_user_info_cursor = db_user_info.cursor(pymysql.cursors.DictCursor)

    sql="select username, email from user_info;"
    db_user_info_cursor.execute(sql)

    emails = db_user_info_cursor.fetchall()
    for i in emails:
        db_auth = i["email"]
        for j in range(2):
            db_auth = hashlib.sha256(db_auth.encode()).hexdigest()
        if db_auth == auth:
            return json.dumps({"error": 0, "username": i["username"]})

    return json.dumps({"error": 1})

@app.route("/recruit")
def recruit():
    return render_template("recruit.html")

@app.route("/matching")
def matching_show():
    return render_template("matching.html")

@app.route("/recommend_list", methods=["POST"])
def recommend_list():
    username = request.get_json()["username"]
    print(username)
    tags = get_tag_username(username)
    return json.dumps({"status": "success", "tags":tags})

@app.route("/profile_img_type", methods=["POST"])
def profile_type():
    username = request.get_json()["username"]
    file = "C:/Users/ksaya/OneDrive/?????? ??????/??????/????????? ??????/????????????/9ham/static/profile_img/profile_"+username+".jpg"
    if os.path.exists(file):
        return json.dumps({"status": "success", "image_type":"jpg"})
    file = "/static/profile_img/profile_"+username+".png"
    if os.path.exists(file):
        return json.dumps({"status": "success", "image_type":"png"})
    else:
        return json.dumps({"status": "failed"})

@app.route("/username_profile", methods=["POST"])
def user_prof():
    lane_n_t = {2:"?????????", 1:"????????????", 0:"??????/???????????? ?????????"}
    username = request.get_json()["username"]
    user_info = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_login")
    user_info_cursor = user_info.cursor(pymysql.cursors.DictCursor)
    sql = "select * from user_info where username='"+str(username)+"';"
    user_info_cursor.execute(sql)
    user_data = user_info_cursor.fetchall()[0]
    email = user_data["email"]
    age = user_data["age"]
    affi = user_data["affi"]
    lane = user_data["lane"]
    lane = lane_n_t[lane]
    checker = user_data["email_check"]
    user_tag = pymysql.connect(user="root", passwd="@dkfldkfl2021@", database="9ham_user_tags")
    user_tag_cursor = user_tag.cursor(pymysql.cursors.DictCursor)
    sql = "select * from user_tags where checker='" + str(checker) + "';"
    user_tag_cursor.execute(sql)
    user_tags = user_tag_cursor.fetchall()[0]["tags"].split(";;")

    return json.dumps({"status":"success","email":email,"age":age,"affi":affi,"lane":lane,"tags":user_tags})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)