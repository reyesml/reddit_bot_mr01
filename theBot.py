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

def runTheBot():
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
				'password': password
				}


	#set the header for all the following requests.  The user-agent should be unique.
	headers = 	{'user-agent': 'My first reddit bot 05182014'}
	 
	#create a requests.session that'll handle our cookies for us
	client = requests.session()

	#request an OAuth token
	r = client.post('https://ssl.reddit.com/api/v1/access_token',headers=headers, auth=client_auth, data=post_data)
	j = json.loads(r.text)
	#store the access_token we receieve from the previous request
	access_token = j['access_token']

	#add the access token to our header for future use
	headers["Authorization"] = 'bearer ' + access_token

	#verify that the token works, by requesting our user data using the access_token in the header
	r = client.get("https://oauth.reddit.com/api/v1/me", headers=headers)

	#Some debugging
	print('-------User Data--------\n', r.json(), '\n------------------')


	#Let's try making a post to /r/FreeKarma.  You WILL need a little
	#bit of link karma before your bot can post without getting stopped
	#by the captcha
	post_data = {
				'api_type': 'json',
				'kind': 'self',
				'sr' : 'FreeKarma',
				'title' : 'Hello, world.',
				'text' : 'Hooray, it works!'
				}

	r = client.post("https://oauth.reddit.com/api/submit", headers=headers, data=post_data)

	#More debugging
	print('----------Submission Response----------\n', r.json(), '\n-------------------')


if __name__ == '__main__':
	runTheBot()
