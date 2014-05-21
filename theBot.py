#importing all the modules
from pprint import pprint
import requests
import requests.auth
import json
import time

#self-imposed waiting time so we don't get our bot locked
#out by making too many requests.
WAIT_TIME = 2


def get_config():
  print('Loading config...')
  json_data = open('config.json', 'r').read()
  config = json.loads(json_data)
  return config

def getOAuthData(session, userName, password, clientID, clientSecret, headers):
	print('Requesting OAuth Token for ', userName, '...')
	data = {
			'grant_type' : 'password',
			'username': userName,
			'password': password
			}
	client_auth = requests.auth.HTTPBasicAuth(clientID, clientSecret)
	r = session.post('https://ssl.reddit.com/api/v1/access_token',headers=headers, auth=client_auth, data=data)
	print(r.headers)
	#hold on to your butts, no error checking here...
	j = json.loads(r.text)
	time.sleep(WAIT_TIME)
	return j


def createSelfPost(session, headers, subReddit, title, body):
	print('Submitting self-post to ', subReddit, '...')
	data =	{
			'api_type': 'json',
			'kind': 'self',
			'sr' : subReddit,
			'title' : title,
			'text' : body
			}
	r = session.post("https://oauth.reddit.com/api/submit", headers=headers, data=data)
	print(r.headers)
	#hold on to your butts, no error checking here...
	j = json.loads(r.text)
	time.sleep(WAIT_TIME)
	return j

def sendPrivateMessage(session, headers, to, subject, body):
	print('Sending message to ', to, '...')
	data = {
			'api_type' : 'json',
			'subject' : subject,
			'text' : body,
			'to' : to
			}
	r = session.post('https://oauth.reddit.com/api/compose',headers=headers, data=data)
	print(r.headers)
	#hold on to your butts, no error checking here...
	j = json.loads(r.text)
	time.sleep(WAIT_TIME)
	return j


def runTheBot():
	#Retrieve the config data
	config = get_config()
	username = config['username']
	password = config['password']
	client_id = config['Client_ID']
	client_secret = config['Client_Secret']
	headers = 	{'user-agent': 'My first reddit bot 05182014'}
	client = requests.session()

	#request an OAuth token
	#timeTokenRequested = time.time() #our token will expire 1 hour from now.
	oauthData = getOAuthData(client, username, password, client_id, client_secret, headers)
	print('Oauth Data: ', oauthData)
	#store the access_token we receieve from the previous request
	access_token = oauthData['access_token']
	#add the access token to our header for future use
	headers["Authorization"] = 'bearer ' + access_token
	#refresh_token = oauthData['refresh_token']
	print('Token 01 ', access_token, ' will expire on: ', oauthData['expires_in'])
	message = 'The current time is {0}'.format(time.asctime())
	resp = sendPrivateMessage(client, headers, '<Test USER>', 'hello, again', message)

	print('Exiting script.')





if __name__ == '__main__':
	runTheBot()
