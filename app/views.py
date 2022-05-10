from time import sleep
import flask_login

from importlib_metadata import method_cache
from app import app 
from flask import render_template
from flask import request , redirect
from flask import send_from_directory,abort
import os


@app.route("/")
@flask_login.login_required
def index():
   
    return render_template("base.html")



@app.route("/API", methods=["GET", "POST"])
def ap():
    

     
     return render_template("public/APIdoc.html")

