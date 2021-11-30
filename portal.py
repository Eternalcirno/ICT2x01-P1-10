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

conn.execute('CREATE TABLE IF NOT EXISTS data_table (data TEXT)')
#conn.execute('DROP TABLE data_table')
#print("Table created successfully")
conn.close()

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
config = dotenv.dotenv_values(dotenv_file)
uname = config["UNAME"]
passwd = config["PASS"]
ratelimit = 0
btime = 0
banned = False

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route("/",methods=["GET"])
def homepage():
    print()
    return render_template("./index.html")

@app.route("/admin", methods=["GET","POST","PUT"])
def admin():
    test = 0
    if request.method == 'POST':  # this block is only entered when the form is submitted
        test = request.args.get('test')
        with sql.connect("database.db") as con:
            cur = con.cursor()
            #cur.execute("INSERT INTO data_table(data) VALUES (0)")
            cur.execute('UPDATE data_table SET data=? WHERE rowid=1',(test,))
            con.commit()
            msg = "Record successfully added"

    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select * from data_table")
        row = cur.fetchone()
        data = row[0]
    return render_template("./admin.html",data=data)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("./admin.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    return render_template("./dashboard.html")

@app.route("/play", methods=["GET","POST"])
def play():
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
    app.run(host='0.0.0.0', port=80)
