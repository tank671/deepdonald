import tweepy
import csv
import time
import re
from fastai import *
from fastai.text import *
from pathlib import Path
from os import environ

INTERVAL = 60*30 # for testing
exec(open("twitter.py").read())

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['RNN_DonaldTrump'], is_async=True)

while True:
    for follower in tweepy.Cursor(api.followers).items():
        follower.follow()
    trump_tweets()
    time.sleep(INTERVAL)
