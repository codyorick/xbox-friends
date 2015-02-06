import sys
import requests
import pymongo

xuid_api = 'https://xboxapi.com/v2/xuid/'
base_api = 'https://xboxapi.com/v2/'

if len(sys.argv) != 3:
    exit("Wrong number of arguments")

user = sys.argv[1]
api_key = sys.argv[2]

xuid_url = xuid_api + user

xauth = {'X-AUTH': api_key}

r = requests.get(xuid_url, headers=xauth)

xuid = r.text

if 'error_code' in xuid:
    print "error"
    sys.exit(-1)

friends_url = base_api + xuid + '/friends'

friends = requests.get(friends_url, headers=xauth)

friends = friends.json()

for f in friends:
    print f['Gamertag']