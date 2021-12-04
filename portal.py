import hashlib
import re
from markupsafe import Markup
from decouple import config
import auth
import json
import sqlite3 as sql
import hashlib
import secrets
import sqlite3 as sql
import time

import dotenv
from flask import *

ratelimit = 0
btime = 0
banned = False

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS speed_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS line_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS distance_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS commands_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS start_robot (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS checkpoint (data TEXT)')
with sql.connect("database.db") as con:
    cur = con.cursor()
    #     cur.execute('INSERT INTO speed_table(data) VALUES(0)')
    #     cur.execute('INSERT INTO line_table(data) VALUES(0)')
    #     cur.execute('INSERT INTO distance_table(data) VALUES(0)')
    cur.execute('INSERT INTO start_robot(data) VALUES(0)')
# conn.execute('DROP TABLE data_table')
# print("Table created successfully")
conn.close()

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
config = dotenv.dotenv_values(dotenv_file)
uname = config["UNAME"]
passwd = config["PASS"]
print(passwd)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
a = auth.Auth(uname, passwd)


@app.route("/", methods=["GET"])
def homepage():
    print()
    return render_template("./homepage.html")


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == 'POST':  # this block is only entered when car posts
        speed = request.args.get('speed')
        line = request.args.get('line')
        distance = request.args.get('distance')
        start_robot = request.args.get('start_robot')
        checkpoint = request.args.get('checkpoint')
        with sql.connect("database.db") as con:
            cur = con.cursor()
            if speed is not None:
                cur.execute('UPDATE speed_table SET data=? WHERE rowid=1', (speed,))
            if line is not None:
                cur.execute('UPDATE line_table SET data=? WHERE rowid=1', (line,))
            if distance is not None:
                cur.execute('UPDATE distance_table SET data=? WHERE rowid=1', (distance,))
            if start_robot is not None:
                cur.execute('UPDATE start_robot SET data=? WHERE rowid=1', (start_robot,))
            if checkpoint is not None:
                cur.execute('UPDATE checkpoint SET data=? WHERE rowid=1', (checkpoint,))
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

        cur.execute("select * from start_robot")
        row = cur.fetchone()
        start_robot = row[0]

        cur.execute("select * from checkpoint")
        row = cur.fetchone()
        checkpoint = row[0]

    return render_template("./data.html", speed=speed, line=line, distance=distance, start_robot=start_robot, checkpoint=checkpoint)


@app.route("/commands", methods=["GET"])
def commands():
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select * from commands_table")
        row = cur.fetchone()
        command = "[" + row[0] + "]"
    # return render_template("./commands.html",command=command)
    return command


@app.route("/start", methods=["GET"])
def start():
    start = "1"
    return render_template("./start.html", start=start)


@app.route("/admin", methods=["GET"])
def admin():
    return render_template("./admin.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("./admin.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select * from commands_table")
        row = cur.fetchone()

        #cur.execute("select * from checkpoint")
        #row = cur.fetchone()
        #checkpoint = row[0]


        command = "[" + row[0] + "]"

        return render_template("./dashboard.html",command=command)
    #return command
    #return render_template("./dashboard.html", speed=speed,checkpoint=checkpoint,)


@app.route("/layout", methods=["GET", "POST"])
def layout():
    return render_template("./layout.html")


@app.route("/play", methods=["GET", "POST"])
def play():
    if (request.method == "POST"):
        cmds = request.get_json()['data']
        with sql.connect("database.db") as con:
            cur = con.cursor()
            # cur.execute('UPDATE start_robot SET data=1 WHERE rowid=1', (cmds,))
            cur.execute('UPDATE commands_table SET data=? WHERE rowid=1', (cmds,))

        print(cmds)
        print(type(cmds))

    return render_template("./play.html")


@app.route("/auth", methods=["POST"])
def login():
    user = request.form.get("login")
    password = request.form.get("password")
    try:
        a.login(user,password)
        flash("Successfully logged in")
        resp = make_response(render_template("./panel.html"))
        session["auth"] = "1"
        return resp
    except NameError as e:
        return str(e)

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
    newpass = request.form.get("newpass")
    cnewpass = request.form.get("cfmnewpass")
    oldpass = request.form.get("oldpass")
    hashed = hashlib.sha256(newpass.encode('utf-8')).hexdigest()
    try:
        a.change(oldpass,newpass,cnewpass,hashed)
        dotenv.set_key(dotenv_file, "PASS", hashed)
        return "password successfully changed"
    except NameError as e:
        return str(e)


if __name__ == "__main__":
    app.run()
