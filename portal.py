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

#@app.route("/",methods=["GET"])
#def adminpage():
 #   print()
  #  return render_template("./index.html")

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("./admin.html")

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


@app.route('/')
def index(app_data=None):
    return render_template('homepage.html', app_data=app_data)


@app.route('/dashboard')
def dashboard(app_data=None):
    return render_template('dashboard.html', app_data=app_data)

@app.route('/control')
def control(app_data=None):
    return render_template('control.html', app_data=app_data)





if __name__ == "__main__":
    app.run()
