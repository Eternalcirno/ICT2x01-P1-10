from flask import *
from markupsafe import Markup
from decouple import config
import dotenv
import re

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
    return render_template("./index.html")

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("./admin.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    return render_template("./dashboard.html")

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
    app.run(debug=True)
