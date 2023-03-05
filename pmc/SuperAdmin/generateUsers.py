import os
import re
import sys
import json
import uuid
import random
import string
import datetime
import base64
sys.path.append('../../')

import bcrypt
from credentials.globalVariables import *
from credentials.tokenInitialization import *
import requests



tables = ['users_by_userid', 'users_by_username', 'users_by_useremail', 'users_by_companyid']
user_columns = ['user_id', 'user_name', 'user_email', 'created_at', 'f_name', 'l_name', 'modified_at', 'user_category', 'user_password', 'user_status', 'user_salt']
company_columns = ['company_id', 'company_name', 'company_status', 'company_website']

#random_company_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
# secret = str(base64.b64encode(password.encode()))[2:-1]

uuid = str(uuid.uuid1())
pmc_company_id = 'UrWMS0v9KDSg2Kx0'
now = str(datetime.datetime.now())
password = 'abc123'
password = password.encode('utf-8')
user_salt = bcrypt.gensalt()
secret = bcrypt.hashpw(password, user_salt)

user_salt = user_salt.decode('utf-8')
secret = secret.decode('utf-8')


value_user_columns = [uuid, 'test', 'test@pmc.com.my', now, 'Test', 'User', now, 'pmc', secret, 'inactive', user_salt]
value_company_columns = [pmc_company_id, 'Project Management Console', 'active', 'pmc.com.my']


existing_userids = []
existing_usernames = []
existing_emails = []
data = {}
payload = []

response_userid = []
response_username = []
response_useremail = []
response_companyid = []


class superAdmin():
	def __inti__(self):
		pass
	def addUser(payloadjson):
		add_row_userid = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + tables[0]
		add_row_username = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + tables[1]
		add_row_useremail = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + tables[2]
		add_row_companyid = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + tables[3]
		headers = {'Accept':'application/json','Content-Type': 'application/json', 'x-cassandra-token': ASTRA_DB_APPLICATION_TOKEN}
		payload_json = json.loads(payloadjson)
		request_userid = requests.post(add_row_userid, headers=headers, json=payload_json)
		request_username = requests.post(add_row_username, headers=headers, json=payload_json)
		request_useremail = requests.post(add_row_useremail, headers=headers, json=payload_json)
		request_companyid = requests.post(add_row_companyid, headers=headers, json=payload_json)
		response_userid_json = request_userid.content.decode()
		response_userid_json = json.loads(response_userid_json)
		response_userid.append(response_userid_json['user_id'])
		response_username_json = request_username.content.decode()
		response_username_json = json.loads(response_username_json)
		response_username.append(response_username_json['user_name'])
		response_useremail_json = request_useremail.content.decode()
		response_useremail_json = json.loads(response_useremail_json)
		response_useremail.append(response_useremail_json['user_email'])
		response_companyid_json = request_companyid.content.decode()
		response_companyid_json = json.loads(response_companyid_json)
		response_companyid.append(response_companyid_json['company_id'])


class data_payload():
	def __init__(self):
		pass
	def payloadGeneration(usercolumns, valueuser, companycolumns, valuecompany):
		user_data = dict(zip(usercolumns, valueuser))
		company_data = dict(zip(companycolumns, valuecompany))
		for item in [user_data, company_data]:
			data.update(item)
		stringData = str(data)
		stringData = stringData.replace("'", '"')
		payload.append(stringData)
		superAdmin.addUser(payload[0])


class checkValueCount():
	def __init__(self):
		pass
	def checkvaluecount(checkuservalues, checkcompanyvalues):
		if len(checkuservalues) == 11:
			if len(checkcompanyvalues) == 4:
				data_payload.payloadGeneration(user_columns, value_user_columns, company_columns, value_company_columns)
			else:
				print("Please check there are exactly 4 elements in value_company_columns list")
		else:
			print("Please check there are exactly 11 elements in value_user_columns list")


class checkCompanyColumns():
	def __init__(self):
		pass
	def companycolumns(companycolumns):
		if len(companycolumns) == 4:
			if companycolumns[0] == "company_id":
				if companycolumns[1] == "company_name":
					if companycolumns[2] == "company_status":
						if companycolumns[3] == "company_website":
							checkValueCount.checkvaluecount(value_user_columns, value_company_columns)
						else:
							print("Please check fourth element in company_columns list")
					else:
						print("Please check third element in company_columns list")
				else:
					print("Please check second element in company_columns list")
			else:
				print("Please check first element in company_columns list")
		else:
			print("Please check total columns in company_columns")


class checkUserColumns():
	def __init__(self):
		pass
	def usercolumns(usercolumns):
		if len(usercolumns) == 11:
			if usercolumns[0] == "user_id":
				if usercolumns[1] == "user_name":
					if usercolumns[2] == "user_email":
						if usercolumns[3] == "created_at":
							if usercolumns[4] == "f_name":
								if usercolumns[5] == "l_name":
									if usercolumns[6] == "modified_at":
										if usercolumns[7] == "user_category":
											if usercolumns[8] == "user_password":
												if usercolumns[9] == "user_status":
													if usercolumns[10] == "user_salt":
														checkCompanyColumns.companycolumns(company_columns)
													else:
														print("Please check eleventh element in user_columns list")
												else:
													print("Please check tenth element in user_columns list")
											else:
												print("Please check ninth element in user_columns list")
										else:
											print("Please check eight element in user_columns list")
									else:
										print("Please check seventh element in user_columns list")
								else:
									print("Please check sixth element in user_columns list")
							else:
								print("Please check fifth element in user_columns list")
						else:
							print("Please check fourth element in user_columns list")
					else:
						print("Please check third element in user_columns list")
				else:
					print("Please check second element in user_columns list")
			else:
				print("Please check first element in user_columns list")
		else:
			print("Please check total columns in user_columns list")


class checkTables():
	def __init__(self):
		pass
	def alltables(table):
		if len(tables) == 4:
			if tables[0] == 'users_by_userid':
				if tables[1] == 'users_by_username':
					if tables[2] == 'users_by_useremail':
						if tables[3] == 'users_by_companyid':
							checkUserColumns.usercolumns(user_columns)
						else:
							print("Please check fourth column spelling")
					else:
						print("Please check third column spelling")
				else:
					print("Please check second column spelling")
			else:
				print("Please check first column")
		else:
			print("Please enter only the required tables")


class checkUsercompany():
	def __init__(self):
		pass
	def usercompany(valuecompanycolumn):
		if valuecompanycolumn == 'UrWMS0v9KDSg2Kx0':
			checkTables.alltables(tables)
		else:
			print("Please put 'UrWMS0v9KDSg2Kx0' in the pmc_company_id variable above")



class checkUseremail():
	def __init__(self):
		pass
	def useremail(tablename, usercolumn, valueusercolumn):
		check_row_useremail = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + tablename + '/rows?fields=' + usercolumn
		headers = {'x-cassandra-token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type':'application/json',}
		check_response = requests.get(check_row_useremail, headers=headers)
		existing_useremails = check_response.json()
		for element in existing_useremails['data']:
			existing_emails.append(element['user_email'])
		if valueusercolumn in existing_emails:
			print("Email already exists, please check user_email in value_user_columns list")
		else:
			checkUsercompany.usercompany(value_company_columns[0])


class checkUsername():
	def __init__(self):
		pass
	def username(tablename, usercolumn, valueusercolumn):
		check_row_username = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + tablename + '/rows?fields=' + usercolumn
		headers = {'x-cassandra-token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type':'application/json',}
		check_response = requests.get(check_row_username, headers=headers)
		existing_unames = check_response.json()
		for element in existing_unames['data']:
			existing_usernames.append(element['user_name'])
		if valueusercolumn in existing_usernames:
			print("Username already exists, please check user_name in value_user_columns list")
		else:
			checkUseremail.useremail(tables[2], user_columns[2], value_user_columns[2])

class checkUserID():
	def __int__(self):
		pass
	def userid(tablename, usercolumn, valueusercolumn):
		check_row_userid = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/keyspaces/' + ASTRA_DB_KEYSPACE + '/' + tablename + '/rows?fields=' + usercolumn
		headers = {'x-cassandra-token': ASTRA_DB_APPLICATION_TOKEN, 'Content-Type':'application/json',}
		check_response = requests.get(check_row_userid, headers=headers)
		existing_ids = check_response.json()
		for element in existing_ids['data']:
			existing_userids.append(element['user_id'])
		if valueusercolumn in existing_userids:
			print("User ID already exists, please check UUID in value_user_columns list")
		else:
			checkUsername.username(tables[1], user_columns[1], value_user_columns[1])



checkUserID.userid(tables[0],user_columns[0], value_user_columns[0])

print('User ID: ' + response_userid[0])
print('Username: ' + response_username[0])
print('User Email: ' + response_useremail[0])
print('Company ID: ' + response_companyid[0])
