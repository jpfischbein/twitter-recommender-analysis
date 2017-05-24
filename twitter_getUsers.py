# Written by Joel Fischbein

from __future__ import print_function
import twitter
import csv

#email account : cmn198twitterbot@gmail.com
#email password: sentiment

CONSUMER_KEY = 'sYdoXdwc2pa1gU5OGRB5aaxXV'
CONSUMER_SECRET = 'zVCdZyZY5bRzDmXuM9Uu4r6EHonxTonJpbLXA4I4Pzitno3JGM'
ACCESS_TOKEN = '857071999100768256-LkWoPQXfC5Yo1j88sylTAHVGNQ6iXeO'
ACCESS_TOKEN_SECRET = '2CGKePsPEgGYDjdjaydE1LppSOjNt4FFHtluXbKPRd5WK'

FOLLOWED_USER = "ucdavis"

# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET,
                  sleep_on_rate_limit=True)

# Function to call to write a row in a csv.
def csv_write(users):
    with open('twitter_davis_followers.csv', 'w') as f:
        writer = csv.writer(f)
        for user in users:
            try:
                user.name.encode('ascii')
            except UnicodeEncodeError:
                continue
            else:
                print(user.name)
                writer.writerow([user.name])

def get_followers():
    return api.GetFriends(screen_name=FOLLOWED_USER)

if __name__ == '__main__':
    print('Start')
    followers = get_followers()
    print('Acquired Followers')
    csv_write(followers)