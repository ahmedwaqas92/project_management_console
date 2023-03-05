import sys
import json
import re
import base64
from flask import Flask, redirect, url_for, Blueprint, render_template, request, session
sys.path.append('../../')

import bcrypt
from credentials.globalVariables import *
from credentials.tokenInitialization import *
import requests


pmc_landing = Blueprint("pmc_landing", __name__, static_url_path="/var/www/html/pmc/pmc/landing/static/", static_folder="static", template_folder="templates")


login_tables = ["users_by_userid", "users_by_username", "users_by_useremail", "users_by_companyid"]
login_fields = ["user_name", "user_email"]
usernames = []
emails = []
user_password = []
user_salt = []
user_fields = []
user_status = []


password_logintables = ['users_by_username', 'users_by_useremail']
password_loginfields = ['user_name', 'user_email']
password_usernames = []
password_emails = []
sending_email = []


@pmc_landing.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username_email = request.form.get("username_email")
        password = request.form.get("password")
        username_endpoint = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + login_tables[1] + '/rows?fields='
        username_endpoint = username_endpoint + login_fields[0]
        headers = {'X-Cassandra-Token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type': 'application/json'}
        data_request = requests.get(username_endpoint, headers=headers)
        data = data_request.json()

        for element in data['data']:
            usernames.append(element['user_name'])
        

        if username_email in usernames:
            username_data_endpoint = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + login_tables[1] + '/'
            username_data_endpoint = username_data_endpoint + username_email
            headers = {'X-Cassandra-Token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type': 'application/json'}
            data_request = requests.get(username_data_endpoint, headers=headers)
            data = data_request.json()

            for element in data['data']:
                user_password.append(element['user_password'])
                user_salt.append(element['user_salt'])
                user_status.append(element['user_status'])

            reverse_usersalt = user_salt[0].encode('utf-8')
            password = password.encode('utf-8')
            hashcheck = bcrypt.hashpw(password, reverse_usersalt).decode('utf-8')
 
            if user_password[0] == hashcheck:
                if user_status[0] == 'active':
                    user_password.clear()
                    user_salt.clear()
                    usernames.clear()
                    user_fields.clear()
                    user_status.clear()

                    for element in data['data']:
                        user_fields.append(element['user_id'])
                        user_fields.append(element['user_name'])
                        user_fields.append(element['user_email'])
                        user_fields.append(element['company_id'])
                        user_fields.append(element['f_name'])
                        user_fields.append(element['l_name'])
                        user_fields.append(element['company_name'])
                        user_fields.append(element['user_category'])

                        session['user_id'] = user_fields[0]
                        session['user_name'] = user_fields[1]
                        session['user_email'] = user_fields[2]
                        session['company_id'] = user_fields[3]
                        session['f_name'] = user_fields[4]
                        session['l_name'] = user_fields[5]
                        session['company_name'] = user_fields[6]
                        session['user_category'] = user_fields[7]

                        if session['user_category'] == 'pmc':
                            return redirect(url_for('pmc_landing.admin_successfulLogin'))
                        elif session['user_category'] == 'director':
                            return redirect(url_for('pmc_landing.director_succesfulLogin'))
                        elif session['user_category'] == 'manager':
                            return redirect(url_for('pmc_landing.manager_successfulLogin'))
                        elif session['user_category'] == 'executive':
                            return redirect(url_for('pmc_landing.executive_successfulLogin'))
                        
                        else:
                            user_password.clear()
                            user_salt.clear()
                            usernames.clear()
                            user_fields.clear()
                            user_status.clear()
                            noUserCategory_modal = True
                            return render_template('landing.html', noUserCategory_modal=noUserCategory_modal)
                else:
                    user_password.clear()
                    user_salt.clear()
                    usernames.clear()
                    user_fields.clear()
                    user_status.clear()
                    noUserActive_modal = True
                    return render_template('landing.html', noUserActive_modal=noUserActive_modal)
            else:
                user_password.clear()
                user_salt.clear()
                usernames.clear()
                user_fields.clear()
                user_status.clear()
                incorrectPass_modal = True
                return render_template('landing.html', incorrectPass_modal=incorrectPass_modal)
            

        else:
            email_endpoint = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + login_tables[2] + '/rows?fields='
            email_endpoint = email_endpoint + login_fields[1]
            headers = {'X-Cassandra-Token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type': 'application/json'}
            data_request = requests.get(email_endpoint, headers=headers)
            data = data_request.json()
            
            for element in data['data']:
                emails.append(element['user_email'])

            if username_email in emails:
                email_data_endpoint = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + login_tables[2] + '/'
                email_data_endpoint = email_data_endpoint + username_email
                headers = {'X-Cassandra-Token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type': 'application/json'}
                data_request = requests.get(email_data_endpoint, headers=headers)
                data = data_request.json()

                for element in data['data']:
                    user_password.append(element['user_password'])
                    user_salt.append(element['user_salt'])
                    user_status.append(element['user_status'])

                reverse_usersalt = user_salt[0].encode('utf-8')
                password = password.encode('utf-8')
                hashcheck = bcrypt.hashpw(password, reverse_usersalt).decode('utf-8')

                if user_password[0] == hashcheck:
                    if user_status[0] == 'active':
                        user_password.clear()
                        user_salt.clear()
                        emails.clear()
                        user_fields.clear()
                        user_status.clear()

                        for element in data['data']:
                            user_fields.append(element['user_id'])
                            user_fields.append(element['user_name'])
                            user_fields.append(element['user_email'])
                            user_fields.append(element['company_id'])
                            user_fields.append(element['f_name'])
                            user_fields.append(element['l_name'])
                            user_fields.append(element['company_name'])
                            user_fields.append(element['user_category'])

                            session['user_id'] = user_fields[0]
                            session['user_name'] = user_fields[1]
                            session['user_email'] = user_fields[2]
                            session['company_id'] = user_fields[3]
                            session['f_name'] = user_fields[4]
                            session['l_name'] = user_fields[5]
                            session['company_name'] = user_fields[6]
                            session['user_category'] = user_fields[7]

                            if session['user_category'] == 'pmc':
                                return redirect(url_for('pmc_landing.admin_successfulLogin'))
                            elif session['user_category'] == 'director':
                                return redirect(url_for('pmc_landing.director_succesfulLogin'))
                            elif session['user_category'] == 'manager':
                                return redirect(url_for('pmc_landing.manager_successfulLogin'))
                            elif session['user_category'] == 'executive':
                                return redirect(url_for('pmc_landing.executive_successfulLogin'))
                            else:
                                user_password.clear()
                                user_salt.clear()
                                usernames.clear()
                                user_fields.clear()
                                user_status.clear()
                                noUserCategory_modal = True
                                return render_template('landing.html', noUserCategory_modal=noUserCategory_modal)
                    
                    else:
                        user_password.clear()
                        user_salt.clear()
                        usernames.clear()
                        user_fields.clear()
                        user_status.clear()
                        noUserActive_modal = True
                        return render_template('landing.html', noUserActive_modal=noUserActive_modal)

                else:
                    user_password.clear()
                    user_salt.clear()
                    usernames.clear()
                    user_fields.clear()
                    user_status.clear()
                    incorrectPass_modal = True
                    return render_template('landing.html', incorrectPass_modal=incorrectPass_modal)
                        
            else:
                user_password.clear()
                user_salt.clear()
                usernames.clear()
                user_fields.clear()
                user_status.clear()
                noUsername_OrEmail = True
                return render_template('landing.html', noUsername_OrEmail=noUsername_OrEmail)


    return render_template("landing.html")


@pmc_landing.route("/admindashboard_route")
def admin_successfulLogin():
    return redirect(url_for('pmc_admindashboard.admin_successfulLogin'))

@pmc_landing.route("/directordashboard_route")
def director_successfulLogin():
    return redirect(url_for('pmc_directordashboard.director_successfulLogin'))

@pmc_landing.route("/managerdashboard_route")
def manager_successfulLogin():
    return redirect(url_for('pmc_managerdashboard.manager_successflLogin'))

@pmc_landing.route("/executivedashboard_route")
def executive_successfulLogin():
    return redirect(url_for('pmc_executivedashboard.executive_successfulLogin'))

@pmc_landing.route("/password_reset", methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        password_useremail = request.form.get("password_useremail")
        username_endpoint = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + password_logintables[0] + '/rows?fields='
        username_endpoint = username_endpoint + password_loginfields[0]
        headers = {'X-Cassandra-Token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type': 'application/json'}
        data_request = requests.get(username_endpoint, headers=headers)
        data = data_request.json()

        for element in data['data']:
            password_usernames.append(element['user_name'])

        if password_useremail in password_usernames:
            username_data_endpoint = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + password_logintables[0] + '/'
            username_data_endpoint = username_data_endpoint + password_useremail
            headers = {'X-Cassandra-Token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type': 'application/json'}
            data_request = requests.get(username_data_endpoint, headers=headers)
            data = data_request.json()

            for element in data['data']:
                sending_email.append(element['user_email'])

                #################################################
                #CODE NEEDED TO GENERATE LINK AND SEND VIA EMAIL#
                #################################################

                emailSent_modal = True
                return render_template('password_reset.html', emailSent_modal=emailSent_modal)

            password_usernames.clear()
            sending_email.clear()

        else:
            email_endpoint = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + password_logintables[1] + '/rows?fields='
            email_endpoint = email_endpoint + password_loginfields[1]
            headers = {'X-Cassandra-Token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type': 'application/json'}
            data_request = requests.get(email_endpoint, headers=headers)
            data = data_request.json()
            
            for element in data['data']:
                password_emails.append(element['user_email'])

            if password_useremail in password_emails:
                email_data_endpoint = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + password_logintables[1] + '/'
                email_data_endpoint = email_data_endpoint + password_useremail
                headers = {'X-Cassandra-Token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type': 'application/json'}
                data_request = requests.get(email_data_endpoint, headers=headers)
                data = data_request.json()

                for element in data['data']:
                    sending_email.append(element['user_email'])
                    
                    #################################################
                    #CODE NEEDED TO GENERATE LINK AND SEND VIA EMAIL#
                    #################################################

                    emailSent_modal = True
                    return render_template('password_reset.html', emailSent_modal=emailSent_modal)

                password_emails.clear()
                sending_email.clear()

            else:
                password_emails.clear()
                sending_email.clear()
                emailNotSent_modal = True
                return render_template('password_reset.html', emailNotSent_modal=emailNotSent_modal)

    return render_template("password_reset.html")

@pmc_landing.route("/register_facebook")
def register_facebook():
	return redirect(url_for('pmc_register.register_facebook'))

@pmc_landing.route("/register_google")
def register_google():
	return redirect(url_for('pmc_register.register_google'))

@pmc_landing.route("/register_email")
def register_email():
	return redirect(url_for('pmc_register.register_email'))
