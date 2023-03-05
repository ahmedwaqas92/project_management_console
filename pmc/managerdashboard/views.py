import sys
import json
import re
from flask import Flask, redirect, url_for, Blueprint, render_template, request, session
sys.path.append('../../')


from credentials.globalVariables import *
from credentials.tokenInitialization import *
import requests




pmc_managerdashboard = Blueprint("pmc_managerdashboard", __name__, static_url_path="/var/www/html/pmc/pmc/managerdashboard/static/", static_folder="static", template_folder="/var/www/html/pmc/pmc/managerdashboard/templates")


@pmc_managerdashboard.route("/managerdashboard")
def manager_successfulLogin():
	return render_template('managerdashboard.html')
