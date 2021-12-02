from flask import *
from markupsafe import Markup
from decouple import config
import dotenv
import time
import re
import secrets
import hashlib
import json
import os
import sqlite3 as sql

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS speed_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS line_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS distance_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS commands_table (data TEXT)')
with sql.connect("database.db") as con:
    cur = con.cursor()
#     cur.execute('INSERT INTO speed_table(data) VALUES(0)')
#     cur.execute('INSERT INTO line_table(data) VALUES(0)')
#     cur.execute('INSERT INTO distance_table(data) VALUES(0)')
#     cur.execute('INSERT INTO commands_table(data) VALUES(0)')
#conn.execute('DROP TABLE data_table')
#print("Table created successfully")
conn.close()


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
config = dotenv.dotenv_values(dotenv_file)
uname = config["UNAME"]
passwd = config["PASS"]
print(passwd)

app = Flask(__name__)

@app.route("/",methods=["GET"])
def homepage():
    print()
    return render_template("./homepage.html")

@app.route("/data",methods=["GET","POST"])
def data():
    if request.method == 'POST':  # this block is only entered when car posts
        speed = request.args.get('speed')
        line = request.args.get('line')
        distance = request.args.get('distance')
        with sql.connect("database.db") as con:
            cur = con.cursor()
            if speed is not None:
                cur.execute('UPDATE speed_table SET data=? WHERE rowid=1',(speed,))
            if line is not None:
                cur.execute('UPDATE line_table SET data=? WHERE rowid=1', (line,))
            if distance is not None:
                cur.execute('UPDATE distance_table SET data=? WHERE rowid=1', (distance,))
            con.commit()

    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select * from speed_table")
        row = cur.fetchone()
        speed = row[0]
        cur.execute("select * from line_table")
        row = cur.fetchone()
        line = row[0]
        cur.execute("select * from distance_table")
        row = cur.fetchone()
        distance = row[0]

    return render_template("./data.html",speed=speed,line=line,distance=distance)

@app.route("/commands", methods=["GET"])
def commands():
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select * from commands_table")
        row = cur.fetchone()
        command = "["+row[0]+"]"
    # return render_template("./commands.html",command=command)
    return command

@app.route("/start", methods=["GET"])
def start():
    start = "1"
    return render_template("./start.html",start=start)

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("./admin.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("./admin.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    return render_template("./dashboard.html")

@app.route("/layout", methods=["GET","POST"])
def layout():
    return render_template("./layout.html")

@app.route("/play", methods=["GET","POST"])
def play():
    if (request.method == "POST"):
        cmds = request.get_json()['data']
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('UPDATE commands_table SET data=? WHERE rowid=1',(cmds,))
        print(cmds)

    return render_template("./play.html")

@app.route("/auth", methods=["POST"])
def login():
    now = time.time()
    global btime
    global ratelimit
    global banned
    if(banned and (now - btime) >= 10):
        ratelimit = 0
        banned = False
    user = request.form.get("login")
    password = request.form.get("password")
    hpassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if(user == ""):
        return "Username cannot be empty"
    if(password == ""):
        return "Password cannot be empty"
    if(user == uname and hpassword == passwd):
        flash("Successfully logged in")
        resp = make_response(render_template("./panel.html"))
        session["auth"] = "1"
        return resp
    if(user != uname or hpassword != passwd):
        if(ratelimit >= 5 and banned == False):
            btime = time.time()
            banned = True
            return "5 invalid tries, account locked out"
        ratelimit += 1
        return "Invalid username or password"

@app.route("/changespeed", methods=["POST"])
def cspeed():
    pass
   # ???

@app.route("/changedist", methods=["POST"])
def cdist():
    pass
   # ???

@app.route("/changepass", methods=["GET","POST"])
def cpass():
    try:
        cookie = session["auth"]
    except:
        return render_template("./admin.html")
    if(cookie == None):
        return render_template("./admin.html")
    if(request.method == "GET"):
        return render_template("./changepass.html")
    print(request.form)
    global passwd
    a = passwd
    oldpass = request.form.get("oldpass")
    holdpass = hashlib.sha256(oldpass.encode('utf-8')).hexdigest()
    newpass = request.form.get("newpass")
    cnewpass = request.form.get("cfmnewpass")
    if(oldpass == newpass):
        return "Old password cannot be the same as new password"
    if(oldpass == ""):
        return "Old password cannot be empty"
    if(newpass == ""):
        return "New password cannot be empty"
    if(cnewpass == ""):
        return "Confirm new password cannot be empty"
    if(holdpass != a):
        return "Incorrect old password"
    elif(newpass != cnewpass):
        return "Passwords do not match"
    elif(not (re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", newpass))):
        return "Password should be 6-20 chars long with upper and lower case characters and special characters"
    elif(holdpass == a):
        hashed = hashlib.sha256(newpass.encode('utf-8')).hexdigest()
        dotenv.set_key(dotenv_file, "PASS", hashed)
        passwd = dotenv.dotenv_values(dotenv_file)["PASS"]
        return "password successfully changed"

if __name__ == "__main__":
    #app.run(host='192.168.43.217', port=80)
    app.run()
