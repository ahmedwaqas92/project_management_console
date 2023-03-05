import sys
import json
import re
from flask import Flask, redirect, url_for, Blueprint, render_template, request, session
sys.path.append('../../')


from credentials.globalVariables import *
from credentials.tokenInitialization import *
import requests




pmc_register = Blueprint("pmc_register", __name__, static_url_path="/var/www/html/pmc/pmc/register/static/", static_folder="static", template_folder="/var/www/html/pmc/pmc/register/templates")


@pmc_register.route("/facebook")
def register_facebook():
	return "<h1>Facebook LOGIN</h1>"

@pmc_register.route("/google")
def register_google():
	return "<h1>Google Login</h1>"

@pmc_register.route("/email", methods=["GET", "POST"])
def register_email():
	if request.method == ["POST"]:
		pass
	return render_template('register_email.html')

@pmc_register.route("/register_cancel")
def register_cancel():
	return redirect(url_for("pmc_landing.home"))
