#Flask app by eloy.acosta@gmail.com

import json
from datetime import timedelta
from flask import Flask, jsonify, request
from hashlib import md5
from pymongo import MongoClient
from pymongo.errors import WriteError
from pymongo.errors import ExecutionTimeout
from dateutil import parser

my_client = MongoClient('mongodb://localhost:27017/')
my_db = my_client.mydatabase
my_collection = my_db.customers

app = Flask(__name__)

#This function validates checksum data types and count
def validate(elem):
	try:
		recv_checksum = elem['md5checksum']
	except (KeyError, NameError, TypeError, RuntimeError) as e:
		app.logger.debug('ERROR Value for key: %s, while trying to get checksum info for: %s' % (e,json.dumps(elem)) )
		return False

	#delete the md5 key-value from the received elem 
	del elem['md5checksum']
	#compare checksum 
	my_checksum = md5(json.dumps(elem)).hexdigest()
	app.logger.debug('El checksum es %s' % my_checksum)

	if recv_checksum == my_checksum:
		#I should check if uid is a number and the date is a date
		try:
			elem['uid'] = int(elem['uid'])
		except (ValueError) as e:
		    app.logger.debug('ERROR: Value error: %s , for the uid: %s' % (e,elem['uid']) )
		    return False
		except (BaseException) as e:
			app.logger.debug('ERROR: %s , for the uid: %s' % (e,elem['uid']) )
			return False
		# Now the date
		try:
			elem['date'] = parser.parse(elem['date'])
		except (ValueError) as e:
			app.logger.debug('ERROR:Value error: %s , for the date: %s' % (elem['date']) )
			return False
		except (BaseException) as e:
			app.logger.debug('ERROR: %s , for the date: %s' % (e,elem['date']) )
			return False
		#All the checks passed and return the element 
		return elem
	else:
		# Cheksum is not valid
		return False

#Create a default index with use instructions 
@app.route('/')
def index():
    return 'Flask is running! Use the correct route to the entry point in the URL'

#Create end point to persist the data. It only accepts http POST method. 
@app.route('/ep1', methods=['POST'])
def mongo_store():
	#It accepts only JSON format data and will only load the json data if the mimetype is application/json 
	my_json = request.get_json(force=True) #Providing Content-Type is no required as force is set to true
	#I check the object type to figure the request object type
	if type(my_json) == list:
		#If it is a list then it shoud be a list of dict elements
		for elem in my_json:
			if type(elem) == dict:
				#Validate checksum and data types for each
				val_element = validate(elem)
				if val_element is False:
					return jsonify(success='false', message='Invalid checksum or field type for some elements')
				#Overwirte element without checksum as I don't want to store it, and with a parsed date format
				elem = val_element
			else:
				# return error as it should be a dict
				return jsonify(success='false', message='Invalid elements in the list')
	elif type(my_json) == dict:
		#I sould be receiving an single element
		val_element = validate(my_json)
		if val_element is False:
			return jsonify(success='false', message='Invalid checksum or field type for some elements')
		#Overwirte element without checksum as I don't want to store it, and with a parsed date format
		#Also convert the payload, as mas mongo insert_many() expects the document as an instance of dict 
		my_json = [val_element]
	else: 
		#Should return an error because of invalid payload
		return jsonify(success='false', message='Invalid payload')

	#Insert into mongo 
	if len(my_json) == 0:
		# There's no payload to save 
		return jsonify(success='false', message='There is no payload to save')
	else:
		# All the checks passed and save json to mongo:
		app.logger.debug(my_json)
		result = my_collection.insert_many(my_json)
		app.logger.debug(result.inserted_ids)
		return jsonify(success='true', message='INFO: %i element/s successfully saved' % len(result.inserted_ids))


@app.route('/ep2', methods=['GET'])
def mongo_query():
	#Verify Query params 
	if request.args.get('uid'):
		try:
			uid = int(request.args.get('uid'))
		except:
			return jsonify(success='false', message='The UID must be an int')
	else:
		return jsonify(success='false', message='A valid UID must be provided')
	
	if request.args.get('date'):
		dateparam = request.args.get('date')
		# I wan't to check if a valid date format is provided
		try:
			date_begin = parser.parse(dateparam)
			date_end = date_begin+timedelta(days=1)
		except:
			return jsonify(success='false', message='Incorrect date format')
	else:
		# If any date is provided will look up all the occurrencies for this UID
		dateparam = ""

	if dateparam != "":
		query_statemet = {'uid' : uid , 'date' : {'$gte' : date_begin, '$lt' : date_end}}
	else:
		query_statemet = {'uid' : uid }

	result = my_collection.find(query_statemet)
	return jsonify(success='true', uid=uid , date=dateparam , count=result.count())

if __name__ == '__main__':
	#WARNING, set debug to false for production proposes.
	app.debug = True
	app.run()
