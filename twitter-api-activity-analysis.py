# Written by Joel Fischbein

from __future__ import print_function
import twitter
import csv

# Information for API Authorized Twitter Account
# email account : cmn198twitterbot@gmail.com
# email password: sentiment

CONSUMER_KEY = 'sYdoXdwc2pa1gU5OGRB5aaxXV'
CONSUMER_SECRET = 'zVCdZyZY5bRzDmXuM9Uu4r6EHonxTonJpbLXA4I4Pzitno3JGM'
ACCESS_TOKEN = '857071999100768256-LkWoPQXfC5Yo1j88sylTAHVGNQ6iXeO'
ACCESS_TOKEN_SECRET = '2CGKePsPEgGYDjdjaydE1LppSOjNt4FFHtluXbKPRd5WK'

SEARCH_TERM = 'delightful'
SEARCH_TERMS = []

# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET,
                  sleep_on_rate_limit=True)

def readin_searches():
	path = './search.csv'
	with open(path, 'rU') as f:
		reader = csv.reader(f)
		for row in reader:
			SEARCH_TERMS.append(row)

# Writes the header in the csv.
def csv_header():
	iofile = open('./twitter.csv','a')
	fields = ('Control', 'Likes', 'Retweets', 'Follows', 'Search')
	fob = csv.DictWriter(iofile, fields, lineterminator = '\n')
	fob.writeheader()

# Function to call to write a row in a csv.
def csv_write(control, likes, retweets, follows, search):
	iofile = open('./twitter.csv','a')
	fields = ('Control', 'Likes', 'Retweets', 'Follows', 'Search')

	fob = csv.DictWriter(iofile, fields, lineterminator = '\n')

	fob.writerow({'Control':control, 'Likes':likes, 'Retweets':retweets, 'Follows':follows, 'Search':search})

# Likes top 100 tweets from search term then retrieves
# recommended users and unlikes tweets
def bias_like():
    # get tweets from searched term
    tweets = api.GetSearch(term=SEARCH_TERM, count=100)

    # like all tweets
    for tweet in tweets:
        tweet = api.GetStatus(tweet.id)
        if not tweet.favorited:
            api.CreateFavorite(status_id=tweet.id)

    # get recommended users
    user_recs = get_rec_users()

    # unlike all tweets
    likes = api.GetFavorites(count=200)
    for like in likes:
        api.DestroyFavorite(status_id=like.id)
    return user_recs

# **************DOESN'T WORK PROPERLY********************
# CAN'T RECOGNIZE WHEN A TWEET HAS BEEN RETWEETED ALREADY
# Retweets top 100 tweets from search term then retrieves
# recommended users and deletes retweets
def bias_retweet():
    # get tweets from search term
    tweets = api.GetSearch(term=SEARCH_TERM, count=100)

    # retweet them all
    # api.PostRetweet(tweets[0].id)
    for tweet in tweets:
        api.PostRetweet(tweet.id)

    # get recommended users
    user_recs = get_rec_users()

    # get retweets
    tweets = api.GetUserRetweets(count=100)

    # delete all retweets
    # api.DestroyStatus(tweets[0].id)
    for tweet in tweets:
        api.DestroyStatus(tweet.id)
    return user_recs

# Follows 100 top users from searched term then retrieves
# recommended users and unfollows all followed users
def bias_follow():
    # get users from search term
    users = api.GetUsersSearch(term=SEARCH_TERM, count=100)

    # follow users from search term
    # api.CreateFriendship(user_id=users[0].id)
    for user in users:
        api.CreateFriendship(user_id=user.id)

    # get recommended users
    user_recs = get_rec_users()

    # unfollow followed users
    # api.DestroyFriendship(user_id=users[0].id)
    for user in users:
        api.DestroyFriendship(user_id=user.id)

    return user_recs

# Searches entire list of terms in file 'search.csv' then returns suggested users
def bias_search():
    readin_searches()
    for i in range(len(SEARCH_TERMS)):
        res = api.GetSearch(term=SEARCH_TERMS[i])

    return get_rec_users()

# Requests recommended users
def get_rec_users():
    # get user categories
    categories = api.GetUserSuggestionCategories()

    user_suggests = []
    # user_suggests = api.GetUserSuggestion(categories[1])

    # for each category get all suggested users
    for cat in categories:
        user_suggests.append(api.GetUserSuggestion(cat))

    return user_suggests

if __name__ == '__main__':
    print("Start")
    u_unbiased = get_rec_users()
    print("Acquired unbiased recommendations")
    u_bias_like = bias_like()
    print("Acquired like biased recommendations")
    u_bias_follow = bias_follow()
    print("Acquired follow biased recommendations")
    u_bias_search = bias_search()
    print("Acquired search history biased recommendations")
    csv_header()
    for i in range(len(u_unbiased)):
        csv_write(u_unbiased[i].name, u_bias_like[i].name,
                  u_bias_retweet[i].name, u_bias_follow[i].name,
                  u_bias_search[i].name)
    print("Done")