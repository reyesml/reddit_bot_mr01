#importing all the modules
from pprint import pprint
import requests
import json
import time
 
#set username and password values
username = 'testUser'
password = 'hunter2'
 
#create dict with username and password
user_pass_dict = {'user': username,
                  'passwd': password,
                  'api_type': 'json'}
 
#set the header for all the following requests
headers = {'user-agent': 'My first reddit bot 05182014' }
 
#create a requests.session that'll handle our cookies for us
client = requests.session()
 
#make a login request, passing in the user and pass as data
r = client.post('http://www.reddit.com/api/login', data=user_pass_dict, headers=headers)
 
#optional print to confirm error-free response
#pprint(r.text)

print('-------Response 1 headers---------\n', r.headers, '\n-------------------')
 
#turns the response's JSON to a native python dict
j = json.loads(r.text)
 
#grabs the modhash from the response
client.modhash = j['json']['data']['modhash']
headers['modhash'] = client.modhash
 
#prints the users modhash
print('{USER}\'s modhash is: {mh}'.format(USER=username, mh=client.modhash))
#time.sleep(3)
r = client.get('http://www.reddit.com/api/me.json', headers=headers)
print('-------Response 2 headers---------\n', r.headers, '\n-------------------')

j2 = json.loads(r.text)
print(j2)
