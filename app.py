
#app.py
from flask import Flask
from datetime import datetime
from flask import request
from flask import jsonify
import time
import pickle

app = Flask(__name__)

#Global variable	
table_of_string = {}
table_of_list = {}
table_of_set = {}


class StringExpire:
	def __init__(self, data):
		self.data = data
		self.timeout = 0
		self.timestamp = 0


	def __init__(self, data, timeout, timestamp):
		self.data = data
		self.timeout = timeout
		self.timestamp = timestamp


	def __repr__(self):
		return self.data + str(self.timeout) + str(self.timestamp)
	def __str__(self):
		return self.data

	def getData(self):
		return self.data

	def getTimeout(self):
		return self.timeout

	def getTimestamp(self):
		return self.timestamp

	def setData(self, data):
		self.data = data

	def setTimeout(self, timeout):
		self.timeout = timeout
		#calculate timestamp here
		ts = time.time()
		self.timestamp = int(ts) + timeout

	def setTimeoutTimestamp(self, timeout, timestamp):
		self.timeout = timeout
		self.timestamp = timestamp




#STRING
@app.route('/SET', methods=['POST'])
def string_set():
    content = request.get_json()
    data = StringExpire(content["value"], 0, 0)
    table_of_string[content["key"]] = data
    return 'SET OK'


@app.route('/GET', methods=['POST'])
def string_get():
    content = request.get_json()
    if content["key"] in table_of_string:
    	return str(table_of_string[content["key"]])
    else :
    	return "ERROR: KEY NOT FOUND"

#LIST
@app.route('/LLEN', methods=['POST'])
def list_len():
	content = request.get_json()
	if content["key"] in table_of_list:
		return str(len(table_of_list[content["key"]]))
	return "ERROR: KEY NOT FOUND"

@app.route('/RPUSH', methods=['POST'])
def list_rpush():
	content = request.get_json()
	list_name = content["key"]
	list_new_data = content["value"].split()



	if list_name in table_of_list:
		raw_list = table_of_list[list_name]
		for value in list_new_data:
			raw_list.append(value)
		table_of_list[list_name] = raw_list
	else :
		new_list = []
		for value in list_new_data:
			new_list.append(value)
		table_of_list[list_name] = new_list

	return str(len(table_of_list[list_name]))

@app.route('/LPOP', methods=['POST'])
def list_pop():
	content = request.get_json()
	list_name = content["key"]
	if list_name in table_of_list:
		list_data = table_of_list[list_name]
		if len(list_data) > 0:
			result = list_data.pop(0)
			return str(result)
		else:
			return "ERROR: LIST EMPTY"
	else:
		return "ERROR: LIST NOT FOUND"

@app.route('/RPOP', methods=['POST'])
def list_rpop():
	content = request.get_json()
	list_name = content["key"]
	if list_name in table_of_list:
		list_data = table_of_list[list_name]
		if len(list_data) > 0:
			last_item = list_data[-1]
			del list_data[-1]
			return str(last_item)
		else:
			return "ERROR: LIST EMPTY"
	else:
		return "ERROR: LIST NOT FOUND"

@app.route('/LRANGE', methods=['POST'])
def list_lrange():
	content = request.get_json()
	list_name = content["key"]
	list_index = content["value"].split()
	start = list_index[0]
	stop = list_index[1]
	if list_name in table_of_list:
		list_value = table_of_list[list_name]
		new_list = list_value[int(start): int(stop) + 1]
		return str(new_list)
	else:
		return "ERROR: LIST NOT FOUND"

#SET
@app.route('/SADD', methods=['POST'])
def set_add():
	content = request.get_json()
	set_name = content["key"]
	list_value = content["value"].split()
	if set_name in table_of_set:
		set_data = table_of_set[set_name]
		for value in list_value:
			set_data.add(value)

	else:
		set_data = set()
		for value in list_value:
			set_data.add(value)
		table_of_set[set_name] = set_data
	return "SUCCESSED"


@app.route('/SCARD', methods=['POST'])
def set_card():
	content = request.get_json()
	set_name = content["key"]
	if set_name in table_of_set:
		return str(len(table_of_set[set_name]))
	else :
		return "ERROR: SET NOT FOUND"


@app.route('/SMEMBERS', methods=['POST'])
def set_member():
	content = request.get_json()
	set_name = content["key"]
	if set_name in table_of_set:
		return str(table_of_set[set_name])
	else:
		return "ERROR: SET NOT FOUND"


@app.route('/SREM', methods=['POST'])
def set_rem():
	content = request.get_json()
	set_name = content["key"]
	list_value = content["value"].split()
	if set_name in table_of_set:
		set_data = table_of_set[set_name]
		for value in list_value:
			set_data.remove(value)
		table_of_set[set_name] = set_data
		return "'DELETE SUCCESSED"
	else:
		return "ERROR: SET NOT FOUND"

@app.route('/SINTER', methods=['POST'])
def set_inter():
	content = request.get_json()
	list_set_name = content["listKey"].split()

	if list_set_name[0] in table_of_set:
		first_set = table_of_set[list_set_name[0]]

	for name in list_set_name:
		if not name in table_of_set:
			return "ERROR: SET " + name + " NOT FOUND"
		else:
			first_set = set.intersection(first_set, table_of_set[name])
	if len(first_set) == 0:
		return "EMPTY RESULT"
	return str(first_set)


#DATA EXPIRATION
@app.route('/KEYS', methods=['POST'])
def set_keys():
	list1 = table_of_string.keys() 
	list2 = table_of_list.keys()
	list3 = table_of_set.keys()
	joined_list = [*list1, *list2, *list3]
	if len(joined_list) == 0:
		return "ERROR: NO KEY EXIST"
	result = '\n'.join(joined_list)
	return result


@app.route('/DEL', methods=['POST'])
def set_del_key():
	content = request.get_json()
	key_name = content["key"]
	table_of_string.pop(key_name, None)
	return "'DELETE SUCCESSED"


@app.route('/FLUSHDB', methods=['POST'])
def set_flushdb():
	table_of_set.clear()
	table_of_string.clear()
	table_of_list.clear()
	return "'DELETED ALL KEY"


@app.route('/EXPIRE', methods=['POST'])
def set_expire():
	content = request.get_json()
	key_name = content["key"]
	key_timeout = content["timeout"]
	if key_name in table_of_string:
		data = table_of_string[key_name]
		data.setTimeout(int(key_timeout))
		table_of_string[key_name] = data
		return key_timeout
	else:
		return "ERROR: KEY NOT FOUND"


@app.route('/TTL', methods=['POST'])
def set_ttl():
	content = request.get_json()
	key_name = content["key"]
	if key_name in table_of_string:
		data = table_of_string[key_name]
		timeEnd = data.getTimestamp()
		curTime = int( time.time())
		return str(timeEnd - curTime)
	else:
		return "ERROR: KEY NOT FOUND"


##### SNAPSHOT##### 
@app.route('/SAVE', methods=['POST'])
def set_save():
	saveFile = open('data.txt', 'w')

	numberString = len(table_of_string)
	saveFile.write("%s\n" % str(numberString))
	for item in table_of_string:
		data = table_of_string[item]
		text = item + ' ' + data.getData() + ' ' + str(data.getTimeout()) + ' ' + str(data.getTimestamp())
		saveFile.write("%s\n" % text)

	saveFile.write("%s\n" % str(len(table_of_list)))
	for item in table_of_list:
		data = table_of_list[item]
		s = ' '.join(data)
		item = item + ' ' + s
		saveFile.write("%s\n" % item)

	saveFile.write("%s\n" % str(len(table_of_set)))
	for item in table_of_set:
		data = table_of_set[item]
		s = ' '.join(data)
		item = item + ' ' + s
		saveFile.write("%s\n" % item)
	return "SAVE OK"

@app.route('/RESTORE', methods=['POST'])
def set_restore():
	saveFile = open('data.txt', 'r')

	line = saveFile.readline()
	if int(line) != 0:
		for i in range(0, int(line)):
			raw_data = saveFile.readline()
			list_data = raw_data.split()
			value = StringExpire(list_data[1], list_data[2], list_data[3])
			table_of_string[list_data[0]] = value

	line = saveFile.readline()
	if int(line) != 0:
		for i in range(0, int(line)):
			data = saveFile.readline()
			list_new_data = data.split()
			list_name = list_new_data[0]
			table_of_list[list_name] = list_new_data[1:]



	line = saveFile.readline()
	if int(line) != 0:
		for i in range(0, int(line)):
			data = saveFile.readline()
			list_new_data = data.split()
			set_name = list_new_data[0]
			table_of_set[set_name] = list_new_data[1:]

	return "restore"


@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)