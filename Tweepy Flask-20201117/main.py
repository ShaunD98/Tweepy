from flask import Flask, render_template, request, json
from analysis import create_my_df
from twitter_auth_mock import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

import tweepy as tweepy

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

app = Flask(__name__)
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

search_term = 'LeBron'


def stream_tweets(search_term):
    data = []  # empty list to which tweet_details obj will be added
    counter = 0  # counter to keep track of each iteration
    for tweet in tweepy.Cursor(api.search, q='\"{}\" -filter:retweets'.format(search_term), count=100, lang='en',
                               tweet_mode='extended').items():
        tweet_details = {}
        tweet_details['name'] = tweet.user.screen_name
        tweet_details['tweet'] = tweet.full_text
        tweet_details['retweets'] = tweet.retweet_count
        tweet_details['location'] = tweet.user.location
        tweet_details['created'] = tweet.created_at.strftime("%d-%b-%Y")
        tweet_details['followers'] = tweet.user.followers_count
        tweet_details['is_user_verified'] = tweet.user.verified
        data.append(tweet_details)

        counter += 1
        if counter == 1000:
            break
        else:
            pass
    with open('{}.json'.format(search_term), 'w') as f:
        json.dump(data, f)
    print('done!')

@app.route('/', methods=['GET', 'POST'])
def process_query():
    if request.method == 'POST':
        query = request.form['query']
        tweets = api.search(q=query)

        return render_template('results.html', tweets=tweets)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    print('Starting to stream...')
    stream_tweets(search_term)
    create_my_df()
    print('finished!')
