import auth
import hashlib
import secrets
import db as db
import dotenv
from flask import *

ratelimit = 0
btime = 0
banned = False


db.reset_database()
print("Opened database successfully")

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
    return render_template("./homepage.html")


@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == 'POST':  # this block is only entered when car posts
        speed = request.args.get('speed')
        line = request.args.get('line')
        distance = request.args.get('distance')
        start_robot = request.args.get('start_robot')
        checkpoint = request.args.get('checkpoint')
        db.update_data(speed, line, distance, start_robot, checkpoint)

    speed = db.get_speed()
    line = db.get_line()
    distance = db.get_distance()
    start_robot = db.get_start()
    checkpoint = db.get_checkpoint()

    return render_template("./data.html", speed=speed, line=line, distance=distance, start_robot=start_robot, checkpoint=checkpoint)


@app.route("/commands", methods=["GET"])
def commands():
    command = db.get_commands()
    return command


@app.route("/admin", methods=["GET"])
def admin():
    return render_template("./admin.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("./admin.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    command = db.get_commands()
    return render_template("./dashboard.html",command=command)


@app.route("/layout", methods=["GET", "POST"])
def layout():
    return render_template("./layout.html")


@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "POST":
        cmds = request.get_json()['data']
        start = request.get_json()['start']
        cmdstr = start + cmds
        db.update_commands(cmdstr)

    return render_template("./play.html")


@app.route("/reset", methods=["POST"])
def reset():
    reset = request.args.get('reset')
    db.update_commands(reset)
    return reset


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
