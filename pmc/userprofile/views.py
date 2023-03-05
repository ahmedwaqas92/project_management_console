import sys
import json
import re
from flask import Flask, redirect, url_for, Blueprint, render_template, request, session
sys.path.append('../../')


from credentials.globalVariables import *
from credentials.tokenInitialization import *
import requests


pmc_userprofile = Blueprint("pmc_userprofile", __name__, static_url_path="/var/www/html/pmc/pmc/userprofile/static/", static_folder="static", template_folder="/var/www/html/pmc/pmc/userprofile/templates")


@pmc_userprofile.route("/userprofile")
def main_userprofile():
	return render_template('userprofile.html')
