import sys
import json
import re
from flask import Flask, redirect, url_for, Blueprint, render_template, request, session
sys.path.append('../../')


from credentials.globalVariables import *
from credentials.tokenInitialization import *
import requests




pmc_executivedashboard = Blueprint("pmc_executivedashboard", __name__, static_url_path="/var/www/html/pmc/executivedashboard/static/", static_folder="static", template_folder="/var/www/html/pmc/executivedashboard/templates")


@pmc_executivedashboard.route("/executivedashboard")
def executive_successfulLogin():
	return render_template('executivedashboard.html')
