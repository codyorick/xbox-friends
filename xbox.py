import sys
import requests
from pymongo import MongoClient

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

    friends_record = {}

    friends_record['gamertag'] = user.lower()

    friends_list = []

    for f in friends:
        friends_list.append(f['Gamertag'])

    friends_record['friends'] = friends_list

    client = MongoClient()
    db = client.xboxdb
    results = db.friendlists.find( { 'gamertag' : friends_record['gamertag'] } )
    if results.count() == 0:
        print "user not found, adding user..."
        db.friendlists.insert(friends_record)
        sys.exit(0)
    else:
        print "user found"
        old_list = set(results[0]['friends'])
        new_list = set(friends_list)
        removed = old_list - new_list
        added = new_list - old_list
        if not removed and not added:
            print "no new or removed friends"
            sys.exit(0)
        if removed:
            print "removals: "
            for f in removed:
                print f
        if added:
            print "new friends: "
            for f in added:
                print f
        db.friendlists.update({'gamertag' : friends_record['gamertag']}, {'$set' : {'friends' : friends_list}})
        print 'updated record'
        sys.exit(0)


if __name__ == "__main__":
    main()