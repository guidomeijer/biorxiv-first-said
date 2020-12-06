# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:24:04 2020

@author: Guido Meijer
"""

import pickle
from functions import word_cleanup
import datetime
import tweepy
import time
from os import environ
from biorxiv_retriever import BiorxivRetriever
br = BiorxivRetriever()

# Authenticate to Twitter
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_KEY_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth)

# Load word library
word_library = pickle.load(open('word_library.obj', 'rb'))

while True:
    # Scrape today's papers
    today = datetime.date.today()
    papers = br.query('limit_from%%3A%s limit_to%%3A%s' % (str(today), str(today)),
                      full_text=False)

    # Extract words
    new_words = set()
    for i in range(len(papers)):
        these_words = word_cleanup(papers[i]['abstract'].split())
        for j, word in enumerate(these_words):
            if word not in word_library:
                new_words.add(word)

    """
    # Update word library
    word_library = word_library | new_words
    file_library = open('word_library.obj', 'wb')
    pickle.dump(word_library, file_library)
    file_library.close()
    """

    # Tweet out new words
    if len(new_words) == 0:
        time.sleep(24 * 60 * 60)  # no new words today, sleep for a day
    else:
        # Tweet out new words equally spaced thoughout the day
        for i, word in enumerate(new_words):
            api.update_status(word)
            time.sleep(int((24 * 60 * 60) / len(new_words)))
