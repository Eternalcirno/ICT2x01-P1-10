from flask import *
from markupsafe import Markup

app = Flask(__name__)

@app.route("/",methods=["GET"])
def homepage():
    return render_template("./LOL.html")

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("./admin.html")

@app.route("/auth", methods=["POST"])
def login():
   # ???

@app.route("/changespeed", methods=["POST"])
def cspeed():
   # ???

@app.route("/changedist", methods=["POST"])
def cdist():
   # ???

@app.route("/changepass", methods=["POST"])
def cpass():
   # ???

if __name__ == "__main__":
    app.run()
