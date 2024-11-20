# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:24:04 2020

@author: Guido Meijer
"""

import pickle
from functions import word_cleanup, context, init_log_files
import datetime
import random
import pandas
import numpy as np
import time
from atproto import Client
from biorxiv_retriever import BiorxivRetriever
br = BiorxivRetriever()
init_log_files()

# Settings
ATTEMPTS = 3  # Number of times to try to query in case of an error
N_postS = 3  # Number of posts to send on each instance (rest goes into backlog)
MIN_HOURS = 3  # Max hours to wait between posts (uniform random pick)
MAX_HOURS = 8  # Max hours to wait between posts (uniform random pick)

# Initialize 
auth_keys = pandas.read_csv('auth.csv')
client = Client()
client.login(auth_keys['email'].values[0], auth_keys['password'].values[0])

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

        # Save to log
        log_file = open('log.txt', 'a')
        log_file.write('\n%s\nFound %d new words in %d papers\n' % (
                    datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                    len(new_words),
                    len(papers)))
        log_file.close()

        # If the amount of new words is more than should be posted, make a random selection
        if len(new_words) > N_postS:

            # Pick random words to post this instance
            word_pick = random.sample(range(len(new_words)), N_postS)
            post_words = np.array(new_words)[word_pick]
            post_abstract_ind = np.array(abstract_index)[word_pick]

            # Save words that weren't picked into backlog
            backlog_words = set(new_words)
            backlog_words.difference_update(set(post_words))
            backlog_file = open('backlog_words.txt', 'a')
            for k, word in enumerate(backlog_words):
                backlog_file.write('%s\n' % word)
            backlog_file.close()
        else:
            # Otherwise, post all words
            post_words = new_words.copy()
            post_abstract_ind = abstract_index.copy()

        # post out new words with some random time lag in between
        print('posting %d words' % len(post_words))
        for i, word in enumerate(post_words):

            # Post word on Bluesky
            client.send_post(text=word)

            sleep_time_secs = int(((np.random.random_sample()
                                    * (MAX_HOURS - MIN_HOURS)) + MIN_HOURS) * (60 * 60))
            print('Posted %s, [%d of %d], sleeping for %d minutes' % (
                                    word, i+1, len(post_words), int(sleep_time_secs / 60)))
            time.sleep(sleep_time_secs)

        # If all goes well break out of while loop
        break

    except Exception as error_message:
        attempt += 1
        print('Attempt %d of %d failed' % (attempt, ATTEMPTS))
        print(error_message)
        error_log = open('log.txt', 'a')
        error_log.write('\n%s\n%s\n' % (datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                                        error_message))
        error_log.close()
