import os

from flask import Flask, render_template
from pmc.landing.views import pmc_landing
from pmc.register.views import pmc_register
from pmc.admindashboard.views import pmc_admindashboard
from pmc.directordashboard.views import pmc_directordashboard
from pmc.managerdashboard.views import pmc_managerdashboard
from pmc.executivedashboard.views import pmc_executivedashboard
from pmc.userprofile.views import pmc_userprofile

from credentials.globalVariables import *
from credentials.tokenInitialization import *

app = Flask(__name__)
app.secret_key = ASTRA_DB_APPLICATION_TOKEN
app.session_cookie_path = '/'


app.register_blueprint(pmc_landing, url_prefix="/pmc")
app.register_blueprint(pmc_register, url_prefix="/pmc/register")
app.register_blueprint(pmc_admindashboard, url_prefix="/pmc/admindashboard")
app.register_blueprint(pmc_directordashboard, url_prefix="/pmc/directordashboard")
app.register_blueprint(pmc_managerdashboard, url_prefix="/pmc/managerdashboard")
app.register_blueprint(pmc_executivedashboard, url_prefix="/pmc/executivedashboard")
app.register_blueprint(pmc_userprofile, url_prefix="/pmc/userprofile")


@app.route("/")
def test():
    return "<h1>NoPrefix</h1>"

if __name__ == '__main__':
    app.run(debug=True)
