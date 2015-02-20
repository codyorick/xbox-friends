import sys
import requests
import pymongo

XUID_API = 'https://xboxapi.com/v2/xuid/'
BASE_API = 'https://xboxapi.com/v2/'


def main():

    if len(sys.argv) != 3:
        exit("Wrong number of arguments")

    user = sys.argv[1]
    api_key = sys.argv[2]

    xuid_url = XUID_API + user

    xauth = {'X-AUTH': api_key}

    r = requests.get(xuid_url, headers=xauth)

    xuid = r.text

    if 'error_code' in xuid:
        print "error"
        sys.exit(-1)

    friends_url = BASE_API + xuid + '/friends'

    friends = requests.get(friends_url, headers=xauth)

    friends = friends.json()

    for f in friends:
        print f['Gamertag']


if __name__ == "__main__":
    main()