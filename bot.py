# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:24:04 2020

@author: Guido Meijer
"""

import pickle
from functions import word_cleanup
import datetime
import random
import pandas
import numpy as np
import tweepy
import time
from biorxiv_retriever import BiorxivRetriever
br = BiorxivRetriever()

# Settings
ATTEMPTS = 3  # Number of times to try to query in case of an error
N_TWEETS = 5  # Number of tweets to send on each instance (rest goes into backlog)
MAX_HOURS = 4  # Max hours to wait between tweets (uniform random pick)

# Authenticate to Twitter
api_keys = pandas.read_csv('keys.csv')
auth = tweepy.OAuthHandler(api_keys.loc[0, 'api_key'], api_keys.loc[0, 'api_key_secret'])
auth.set_access_token(api_keys.loc[0, 'access_token'], api_keys.loc[0, 'access_token_secret'])

# Create API object
api = tweepy.API(auth)

# Load word library
word_library = pickle.load(open('word_library.obj', 'rb'))

attempt = 0
while attempt <= ATTEMPTS:
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
        file_library = open('word_library.obj', 'wb')
        pickle.dump(word_library, file_library)
        file_library.close()

        # If the amount of new words is more than should be tweeted, make a random selection
        if len(new_words) > N_TWEETS:

            # Pick random words to tweet this instance
            tweet_words = random.sample(new_words, N_TWEETS)

            # Save words that weren't picked into backlog
            new_words.difference_update(tweet_words)
            backlog_words = pickle.load(open('backlog_words.obj', 'rb'))
            backlog_words = backlog_words | new_words
            backlog_file = open('backlog_words.obj', 'wb')
            pickle.dump(backlog_words, backlog_file)
            backlog_file.close()
        else:
            # Otherwise, tweet all words
            tweet_words = new_words.copy()

        # Tweet out new words with some random time lag in between
        for i, word in enumerate(tweet_words):
            api.update_status(word)
            sleep_time_secs = int((np.random.random_sample() * MAX_HOURS) * (60 * 60))
            print('Tweeted %s, [%d of %d], sleeping for %d minutes' % (
                                    word, i+1, len(tweet_words), int(sleep_time_secs / 60)))
            time.sleep(sleep_time_secs)

	# If all goes well break out of while loop
        break

    except Exception as error_message:
        attempt += 1
        print('Attempt %d of %d failed' % (attempt, ATTEMPTS))
        print(error_message)
        error_log = open('error_log.txt', 'a')
        error_log.write('\n%s\n%s\n' % (datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                                        error_message))
        error_log.close()


