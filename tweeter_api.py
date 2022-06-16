from os import access
import tweepy
import configparser
from tokens import tokens
import pandas as pd

api_key=tokens['API Key']
api_key_secret=tokens['API Key Secret']
bearer_token=tokens['Bearer Token']
access_token=tokens['Access Token']
access_token_secret=tokens['Access Token Secret']


# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()

# create dataframe
columns = ['Time', 'User', 'Tweet']
data = []
for tweet in public_tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

df = pd.DataFrame(data, columns=columns)

df.to_csv('tweets.csv')