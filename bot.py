# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:24:04 2020

@author: Guido Meijer
"""

import pickle
from functions import word_cleanup, context
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
N_TWEETS = 3  # Number of tweets to send on each instance (rest goes into backlog)
MIN_HOURS = 3  # Max hours to wait between tweets (uniform random pick)
MAX_HOURS = 8  # Max hours to wait between tweets (uniform random pick)

# Initialize Twitter API for @bioRxiv_first
api_keys = pandas.read_csv('keys.csv')
auth = tweepy.OAuthHandler(api_keys.loc[0, 'api_key'], api_keys.loc[0, 'api_key_secret'])
auth.set_access_token(api_keys.loc[0, 'access_token'], api_keys.loc[0, 'access_token_secret'])
api_first = tweepy.API(auth)

# Initialize Twitter API for @bioRxiv_where
api_keys = pandas.read_csv('where_keys.csv')
auth = tweepy.OAuthHandler(api_keys.loc[0, 'api_key'], api_keys.loc[0, 'api_key_secret'])
auth.set_access_token(api_keys.loc[0, 'access_token'], api_keys.loc[0, 'access_token_secret'])
api_where = tweepy.API(auth)

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
        new_words = []
        abstract_index = []
        for i in range(len(papers)):
            these_words = word_cleanup(papers[i]['abstract'].split())
            for j, word in enumerate(these_words):
                if word not in word_library:
                    new_words.append(word)
                    abstract_index.append(i)

        # Update word library
        print('Found %d new words' % len(new_words))
        word_library = word_library | set(new_words)
        file_library = open('word_library.obj', 'wb')
        pickle.dump(word_library, file_library)
        file_library.close()

        # If the amount of new words is more than should be tweeted, make a random selection
        if len(new_words) > N_TWEETS:

            # Pick random words to tweet this instance with a maximum of two hyphenated words
            word_pick = random.sample(range(len(new_words)), N_TWEETS)
            tweet_words = new_words[word_pick]
            tweet_abstract_ind = abstract_index[word_pick]
            t = time.time()  # to prevent infinite loop
            while ((len([word for word in tweet_words if word.count('-') > 0]) > 2)
                   and (time.time() - t < 5)):
                word_pick = random.sample(range(len(new_words)), N_TWEETS)
                tweet_words = new_words[word_pick]
                tweet_abstract_ind = abstract_index[word_pick]

            # Save words that weren't picked into backlog
            backlog_words = set(new_words)
            backlog_words.difference_update(set(tweet_words))
            backlog_file = open('backlog_words.txt', 'a')
            for k, word in enumerate(backlog_words):
                backlog_file.write('%s\n' % word)
            backlog_file.close()
        else:
            # Otherwise, tweet all words
            tweet_words = new_words.copy()
            tweet_abstract_ind = abstract_index.copy()

        # Tweet out new words with some random time lag in between
        print('Tweeting %d words' % len(tweet_words))
        for i, word in enumerate(tweet_words):
            # Tweet word on @bioRxiv_first
            word_tweet = api_first.update_status(word)

            # Tweet reply with link to article on @bioRxiv_where
            context_string = context(papers[tweet_abstract_ind[i]]['abstract'], word)
            reply_text = '\"%s\" \n %s' % (context_string, papers[i]['biorxiv_url'])
            print(word_tweet.id)
            api_where.update_status(reply_text, in_reply_to_status_id=word_tweet.id,
                                    auto_populate_reply_metadata=True)

            sleep_time_secs = int(((np.random.random_sample()
                                    * (MAX_HOURS - MIN_HOURS)) + MIN_HOURS) * (60 * 60))
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
