#importing all the modules
from pprint import pprint
import requests
import requests.auth
import json


def get_config():
  print('Loading config')
  json_data = open('config.json', 'r').read()
  config = json.loads(json_data)
  return config

#Retrieve the config data
config = get_config()
username = config['username']
password = config['password']
client_id = config['Client_ID']
client_secret = config['Client_Secret']

#build the auth data
client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)


post_data = {
			  'grant_type' : 'password',
			  'username': username,
              'password': password,
              }


#set the header for all the following requests.  The user-agent should be unique.
headers = 	{'user-agent': 'My first reddit bot 05182014'}
 
#create a requests.session that'll handle our cookies for us
client = requests.session()

#request an OAuth token
r = client.post('https://ssl.reddit.com/api/v1/access_token',headers=headers, auth=client_auth, data=post_data)

print('-------Response 2 headers---------\n', r.headers, '\n-------------------')
j = json.loads(r.text)
print('---Response 2 Body-----')
print(j)

#store the access_token we receieve from the previous request
access_token = j['access_token']

#add the access token to our header for future use
headers["Authorization"] = 'bearer ' + access_token

#verify that the token works, by requesting our user data using the access_token in the header
r = client.get("https://oauth.reddit.com/api/v1/me", headers=headers)

print('-------User Data--------\n', r.json(), '\n------------------')

