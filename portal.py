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

@app.route("/changepass", methods=["POST"])
def cpass():
    pass
   # ???

if __name__ == "__main__":
    app.run()
