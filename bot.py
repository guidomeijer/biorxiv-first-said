# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:24:04 2020

@author: Guido Meijer
"""

import pickle
from functions import word_cleanup
import datetime
import pandas
import numpy as np
import tweepy
import time
from biorxiv_retriever import BiorxivRetriever
br = BiorxivRetriever()

# Authenticate to Twitter
api_keys = pandas.read_csv('keys.csv')
auth = tweepy.OAuthHandler(api_keys.loc[0, 'api_key'], api_keys.loc[0, 'api_key_secret'])
auth.set_access_token(api_keys.loc[0, 'access_token'], api_keys.loc[0, 'access_token_secret'])

# Create API object
api = tweepy.API(auth)

# Load word library
word_library = pickle.load(open('word_library.obj', 'rb'))

try:
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

    # Update word library
    word_library = word_library | new_words
    file_library = open('new_word_library.obj', 'wb')
    pickle.dump(word_library, file_library)
    file_library.close()

    # Tweet out new words
    if len(new_words) > 0:
        # Tweet out new words with some random time lag in between
        for i, word in enumerate(new_words):
            api.update_status(word)
            sleep_time_secs = int((np.random.random_sample() * 2) * (60 * 60))
            print('Tweeted %s, [%d of %d], sleeping for %d minutes' % (word, i+1, len(new_words),
                                                                       int(sleep_time_secs/60)))
            time.sleep(sleep_time_secs)

except Exception as error_message:
    print(error_message)
    error_log = open('error_log.txt', 'a')
    error_log.write('\n%s\n%s\n' % (datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                                    error_message))
    error_log.close()
