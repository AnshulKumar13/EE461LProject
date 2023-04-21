import logging
import sys
import databaseAPI as db
from flask import Flask, session, redirect, url_for, request, render_template
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "asdlkjfh2345io87ewarkjfh"

def clearSession():
    session["username"] = None
    session["projectid"] = None
    session["projectname"] = None
    session["projectdesc"] = None

@app.route("/")
def hello():
    clearSession()
    return render_template('home.html')

@app.route("/signup", methods=["GET","POST"])
def signUp():
    creds = request.form
    if db.addNewUser(creds["username"], creds["password"]):
        session["username"] = creds["username"]
        return redirect("/profile")
    return redirect("/")

@app.route("/signin", methods=["GET","POST"])
def signIn():
    creds = request.form
    if db.authenticateUser(creds["username"], creds["password"]):
        session["username"] = creds["username"]
        return redirect("/profile")
    return redirect("/")

@app.route("/profile", methods=["GET","POST"])
def profile():
    return render_template("profile.html", result=session["username"])

@app.route("/createproject", methods=["GET","POST"])
def createProject():
    info = request.form
    if db.addNewProject(session["username"], info["projectid"], 
                        info["projectname"], info["projectdesc"]):
        session["projectid"] = info["projectid"]
        session["projectname"] = info["projectname"]
        session["projectdesc"] = info["projectdesc"]
        return redirect("/project/" + info["projectname"])
    return redirect("/profile")

@app.route("/openproject", methods=["GET","POST"])
def openProject():
    info = request.form
    prID = info["projectid"]
    if db.authenticateProject(session["username"], prID):
        prInfo = db.getProjectInfo(prID)
        session["projectid"] = prID
        session["projectname"] = prInfo[0]
        session["projectdesc"] = prInfo[2]
        return redirect("/project/" + session["projectname"])
    return redirect("/profile")

@app.route("/project/<name>", methods=["GET","POST"])
def project(name):
    value = {"projectid":session["projectid"], 
             "projectname":session["projectname"], 
             "projectdesc":session["projectdesc"],
             "HW1Amount":db.getHardware("HW1")[0],
             "HW1Capacity":db.getHardware("HW1")[1],
             "HW2Amount":db.getHardware("HW2")[0],
             "HW2Capacity":db.getHardware("HW2")[1]}
    return render_template("projectmanager.html", value=value)

@app.route("/checkout/<num>", methods=["GET","POST"])
def checkout(num):
    amount = request.form["request"]
    db.checkoutHardware("HW" + num, int(amount), session["projectid"])
    return redirect("/project/" + session["projectname"])

if __name__ == "__main__":
    app.run()