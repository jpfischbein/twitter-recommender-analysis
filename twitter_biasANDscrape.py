# Written by Joel Fischbein
#email account : cmn198twitterbot@gmail.com
#email password: sentiment

from __future__ import print_function
from time import sleep
import twitter
import csv

CONSUMER_KEY = 'sYdoXdwc2pa1gU5OGRB5aaxXV'
CONSUMER_SECRET = 'zVCdZyZY5bRzDmXuM9Uu4r6EHonxTonJpbLXA4I4Pzitno3JGM'
ACCESS_TOKEN = '857071999100768256-LkWoPQXfC5Yo1j88sylTAHVGNQ6iXeO'
ACCESS_TOKEN_SECRET = '2CGKePsPEgGYDjdjaydE1LppSOjNt4FFHtluXbKPRd5WK'

BIAS_USERS = []

# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET,
                  sleep_on_rate_limit=True)

def readin_users():
    path = './users.csv'
    with open(path, 'rU') as f:
        reader = csv.reader(f)
        for row in reader:
            BIAS_USERS.append(row)

# Function to call to write a row in a csv.
def csv_write(users):
    with open('./twitter_rec_users.csv','w') as f:
        writer = csv.writer(f)
        for user in users:
            try:
                user.name.encode('ascii')
            except UnicodeEncodeError:
                continue
            else:
                # print(user.name)
                writer.writerow([user.name])


# For stalling till rate limit resets
def stall(mins):
    sleep(mins * 60)

# Requests recommended users
def get_rec_users():
    # get user categories
    categories = api.GetUserSuggestionCategories()
    # print(len(categories))

    user_suggests = []
    # user_suggests = api.GetUserSuggestion(categories[1])
    # print(len(user_suggests))

    # for each category get all suggested users
    for cat in categories:
        user_suggests.append(api.GetUserSuggestion(cat))

    return user_suggests

# Follows users from BIAS_USERS list
def bias_follow():
    # follow users from BIAS_USERS list
    for biasUser in BIAS_USERS:
        # print(biasUser[0])
        user = api.GetUser(screen_name=biasUser[0])
        api.CreateFriendship(user_id=user.id)

    rec_users = get_rec_users()

    for biasUser in BIAS_USERS:
        user = api.GetUser(screen_name=biasUser[0])
        api.DestroyFriendship(user_id=user.id)

    return rec_users

if __name__ == '__main__':
    print('Start')
    readin_users()
    # print(BIAS_USERS)
    print('Read in bias users')
    recs = bias_follow()
    print('Got recommended users')
    csv_write(recs)
    print('Done')
