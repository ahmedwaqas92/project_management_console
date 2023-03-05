import sys
import json
import re
from flask import Flask, redirect, url_for, Blueprint, render_template, request, session
sys.path.append('../../')


from credentials.globalVariables import *
from credentials.tokenInitialization import *
import requests
from flask_paginate import Pagination, get_page_parameter




pmc_admindashboard = Blueprint("pmc_admindashboard", __name__, static_url_path="/var/www/html/pmc/pmc/admindashboard/static/", static_folder="static", template_folder="/var/www/html/pmc/pmc/admindashboard/templates")


@pmc_admindashboard.route("/")
def admin_successfulLogin():
        if 'user_id' in session:
                return redirect(url_for('pmc_admindashboard.dashboard'))
        else:
                return redirect(url_for('pmc_landing.home'))
        
@pmc_admindashboard.route("/dashboard")
def dashboard():
        if 'user_id' in session:
                return render_template('admindashboard_dashboard.html', data=session['user_name'])
        else:
                return redirect(url_for('pmc_landing.home'))        

@pmc_admindashboard.route("/addcompany", methods=["GET"])
def add_company():
        if 'user_id' in session:
                data = ['Speedmax Solutions Sdn Bhd', 'DCS Communications Pvt Ltd', 'Microsoft Corporation Digital Services Sdn Bhd', 'Motorola Company Sdn Bhd', 'AirAsia Sdn Bhd', 'Test6', 'Test7', 'Test8', 'Test9', 'Test10', 'Test11', 'Test12', 'Test13', 'Test14', 'Test15', 'Test16', 'Test17', 'Test18', 'Test19', 'Test20', 'Speedmax Solutions Sdn Bhd', 'DCS Communications Pvt Ltd', 'Microsoft Corporation Digital Services Sdn Bhd', 'Motorola Company Sdn Bhd', 'AirAsia Sdn Bhd', 'Test6', 'Test7', 'Test8', 'Test9', 'Test10', 'Test11', 'Test12', 'Test13', 'Test14', 'Test15', 'Test16', 'Test17', 'Test18', 'Test19', 'Test20', 'Speedmax Solutions Sdn Bhd', 'Speedmax Solutions Sdn Bhd', 'DCS Communications Pvt Ltd', 'Microsoft Corporation Digital Services Sdn Bhd', 'Motorola Company Sdn Bhd', 'AirAsia Sdn Bhd', 'Test6', 'Test7', 'Test8', 'Test9', 'Test10', 'Test11', 'Test12', 'Test13', 'Test14', 'Test15', 'Test16', 'Test17', 'Test18', 'Test19', 'Test20', 'Speedmax Solutions Sdn Bhd', 'DCS Communications Pvt Ltd', 'Microsoft Corporation Digital Services Sdn Bhd', 'Motorola Company Sdn Bhd', 'AirAsia Sdn Bhd', 'Test6', 'Test7', 'Test8', 'Test9', 'Test10', 'Test11', 'Test12', 'Test13', 'Test14', 'Test15', 'Test16', 'Test17', 'Test18', 'Test19', 'Test20', 'Speedmax Solutions Sdn Bhd']
                employees = ['10', '44', '99', '150', '86', '189', '95', '77', '900', '10', '189', '95', '77', '900', '10', '189', '95', '77', '900', '10', '10', '44', '99', '150', '86', '189', '95', '77', '900', '10', '189', '95', '77', '900', '10', '189', '95', '77', '900', '10', '10', '10', '44', '99', '150', '86', '189', '95', '77', '900', '10', '189', '95', '77', '900', '10', '189', '95', '77', '900', '10', '10', '44', '99', '150', '86', '189', '95', '77', '900', '10', '189', '95', '77', '900', '10', '189', '95', '77', '900', '10', '10']
                zipped = zip(data, employees)
                
                page_cal = list(zipped)
                page = request.args.get(get_page_parameter(), type=int, default=1)
                per_page = 4
                total_pages = len(page_cal) // per_page + (len(page_cal) % per_page > 0)
                start = (page - 1) * per_page
                end = start + per_page
                items = page_cal[start:end]
                pagination = Pagination(page=page, total=len(page_cal), per_page=per_page, css_framework="bootstrap5", max_page_links=5)

                return render_template('admindashboard_addcompany.html', items=items, pagination=pagination)
        else:
                return redirect(url_for('pmc_landing.home'))


@pmc_admindashboard.route("/addemployee")
def add_employee():
        if 'user_id' in session:
                return render_template('admindashboard_addemployee.html', data=session['user_email'])
        else:
                return redirect(url_for('pmc_landing.home'))


@pmc_admindashboard.route("/reports")
def reports():
        if 'user_id' in session:
                return render_template('admindashboard_reports.html', data=session['company_id'])
        else:
                return redirect(url_for('pmc_landing.home'))


@pmc_admindashboard.route("/backup")
def backup():
        if 'user_id' in session:
                return render_template('admindashboard_backup.html', data=session['f_name'])
        else:
                return redirect(url_for('pmc_landing.home'))


@pmc_admindashboard.route("/profile")
def profile():
        if 'user_id' in session:
                return render_template('admindashboard_profile.html', data=session['l_name'])
        else:
                return redirect(url_for('pmc_landing.home'))


@pmc_admindashboard.route("/logout")
def logout():
        if 'user_category' in session:                  #If Last session is True then check 1st Session
                if 'user_id' in session:                #If 1st session is True, logout everything
                        session.pop('user_id', None)
                        session.pop('user_name', None)
                        session.pop('user_email', None)
                        session.pop('company_id', None)
                        session.pop('f_name', None)
                        session.pop('l_name', None)
                        session.pop('company_name', None)
                        session.pop('user_category', None)
                        return redirect(url_for('pmc_landing.home'))
                else:
                        return redirect(url_for('pmc_landing.home'))
        else:
                return redirect(url_for('pmc_landing.home'))
