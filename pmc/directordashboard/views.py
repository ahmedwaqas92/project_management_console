import sys
import json
import re
from flask import Flask, redirect, url_for, Blueprint, render_template, request, session
sys.path.append('../../')


from credentials.globalVariables import *
from credentials.tokenInitialization import *
import requests




pmc_directordashboard = Blueprint("pmc_directordashboard", __name__, static_url_path="/var/www/html/pmc/pmc/directordashboard/static/", static_folder="static", template_folder="/var/www/html/pmc/pmc/directordashboard/templates")


@pmc_directordashboard.route("/directordashboard")
def director_successfulLogin():
	return render_template('directordashboard.html')
