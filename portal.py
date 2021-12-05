from flask import *
from markupsafe import Markup
from decouple import config
import dotenv
import re
import json
<<<<<<< Updated upstream
=======
import os
import sqlite3 as sql

ratelimit = 0
btime = 0
banned = False

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('DROP TABLE IF EXISTS speed_table')
conn.execute('DROP TABLE IF EXISTS line_table')
conn.execute('DROP TABLE IF EXISTS distance_table')
conn.execute('DROP TABLE IF EXISTS commands_table')
conn.execute('CREATE TABLE IF NOT EXISTS speed_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS line_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS distance_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS commands_table (data TEXT)')

with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute('INSERT INTO speed_table(data) VALUES(0)')
    cur.execute('INSERT INTO line_table(data) VALUES(0)')
    cur.execute('INSERT INTO distance_table(data) VALUES(0)')
    cur.execute('INSERT INTO commands_table(data) VALUES(0)')
conn.close()

>>>>>>> Stashed changes

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
config = dotenv.dotenv_values(dotenv_file)
uname = config["UNAME"]
passwd = config["PASS"]

app = Flask(__name__)

@app.route("/",methods=["GET"])
def homepage():
    print()
<<<<<<< Updated upstream
    return render_template("./index.html")
=======
    return render_template("./homepage.html")

@app.route("/data",methods=["GET","POST"])
def data():
    if request.method == 'POST':  # this block is only entered when car posts
        speed = request.args.get('speed')
        line = request.args.get('line')
        distance = request.args.get('distance')
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('UPDATE speed_table SET data=? WHERE rowid=1',(speed,))
            cur.execute('UPDATE line_table SET data=? WHERE rowid=1', (line,))
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

        cur.execute("select * from start_robot")
        row = cur.fetchone()
        start_robot = row[0]

    return render_template("./data.html",speed=speed,line=line,distance=distance,start_robot=start_robot)

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
>>>>>>> Stashed changes

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("./admin.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    return render_template("./dashboard.html")

@app.route("/play", methods=["GET","POST"])
def play():
<<<<<<< Updated upstream
    if (request.method == "POST"):
        cmds = request.get_json()['data']
        cmda = cmds.split("+")
        for i in cmda:
            #do robot stuff
            pass
=======
    if request.method == "POST":
        commands = request.get_json()['data']
        start = request.get_json()['start']
        play_str = start + commands
        with sql.connect("database.db") as con:
            cur = con.cursor()
            #cur.execute('UPDATE start_robot SET data=1 WHERE rowid=1', (cmds,))
            #cur.execute('UPDATE commands_table SET data=0 WHERE rowid=1')
            cur.execute('UPDATE commands_table SET data=? WHERE rowid=1', (play_str,))
        print(play_str)

>>>>>>> Stashed changes
    return render_template("./play.html")

@app.route("/reset", methods=["GET","POST"])
def resetcmd():
    if request.method == "POST":
        reset = request.args.get('reset')
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('UPDATE commands_table SET data=? WHERE rowid=1', (reset,))
    return reset

@app.route("/auth", methods=["POST"])
def login():
    pass
   # ???

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
    if(request.method == "GET"):
        return render_template("./changepass.html")
    print(request.form)
    oldpass = request.form.get("oldpass")
    newpass = request.form.get("newpass")
    cnewpass = request.form.get("cfmnewpass")
    if(oldpass != passwd):
        return "incorrect old password"
    elif(newpass != cnewpass):
        return "passwords do not match"
    elif(not (re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", newpass))):
        return "password should be 6-20 chars long with upper and lower case characters and special characters"
    elif(oldpass == passwd):
        dotenv.set_key(dotenv_file, "PASS", newpass)
        global config 
        config = dotenv.dotenv_values(dotenv_file)
        return "password successfully changed"

if __name__ == "__main__":
<<<<<<< Updated upstream
    app.run(debug=True)
=======
    app.run(host='192.168.43.217', port=80)
    #app.run()
>>>>>>> Stashed changes
