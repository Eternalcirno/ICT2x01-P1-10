from flask import *
from markupsafe import Markup
from decouple import config
import auth
import json
import sqlite3 as sql
import hashlib
import dotenv
import secrets

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS speed_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS line_table (data TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS distance_table (data TEXT)')
# with sql.connect("database.db") as con:
#     cur = con.cursor()
#     cur.execute('INSERT INTO speed_table(data) VALUES(0)')
#     cur.execute('INSERT INTO line_table(data) VALUES(0)')
#     cur.execute('INSERT INTO distance_table(data) VALUES(0)')
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
app.secret_key = secrets.token_hex(32)
a = auth.Auth(uname, passwd)

@app.route("/",methods=["GET"])
def homepage():
    print()
    return render_template("./homepage.html")

@app.route("/data",methods=["GET","POST"])
def data():
    if request.method == 'POST':  # this block is only entered when the form is submitted
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
    command = str(123456)
    return render_template("./commands.html",command=command)

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
        cmda = cmds.split("+")
        for i in cmda:
            #do robot stuff
            pass
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
    #app.run(host='0.0.0.0', port=80)
    app.run()
