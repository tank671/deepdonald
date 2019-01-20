import tweepy
import csv
import time
import re
from fastai import *
from fastai.text import *
from pathlib import Path
from os import environ

path = Path('.')

trump_lm = TextLMDataBunch.load(path, 'trump_lm')
data_bunch = (TextList.from_csv(path, csv_name='blank.csv', vocab=trump_lm.vocab)
             .random_split_by_pct()
             .label_for_lm()
             .databunch(bs=10))
learn = language_model_learner(data_bunch, pretrained_model=None)
learn.load('trump_all')

exec(open("textfuncs.py").read())
exec(open("config").read())

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def generateTweet(starter='xxbos', printing=True, publish=False):
    mytext = rawPredict(starter, 80)
    mytext = cleanText(mytext, True)
    mytext = trimText(mytext, True)
    if mytext:
        if printing:
            print(mytext)
        if publish:
            api.update_status(mytext)
    else:
        generateTweet(starter, printing, publish)

def respondTweet(text, user, msg_id):
    starter = " ".join(text)
    mytext = rawPredict(starter, 80)
    mytext = cleanText(mytext, for_twitter=True)
    mytext = trimText(mytext, 0, for_twitter=True)
    if mytext:
        tweet = "@" + str(user) + " " + mytext
        api.update_status(tweet, msg_id, True)
        print(tweet)
    else:
        respondTweet(text, user, msg_id)

def trump_tweets():
    tweetstorm = (random.random() < 0.3)
    if tweetstorm:
        num = random.randint(2,8)
    else:
        num = 1
    for i in range(num):
        generateTweet(printing=True, publish=True)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.text.split()[0] == '@RNN_DonaldTrump':
            user = status.user.screen_name
            msg_id = status.id
            starter = status.text.split()[1:]
            respondTweet(starter, user, msg_id)
