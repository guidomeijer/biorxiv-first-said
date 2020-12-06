# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:24:04 2020

@author: Guido Meijer
"""

import sys
import pickle
from functions import word_cleanup
import datetime
from biorxiv_retriever import BiorxivRetriever
br = BiorxivRetriever()

# Settings
TO_DATE = '2013-11-01'

if len(sys.argv) == 1:
    from_date = datetime.datetime.now().strftime("%Y-%m-%d")  # today
else:
    from_date = sys.argv[1]

# Load current word library
word_library = pickle.load(open('word_library.obj', 'rb'))

date_now = datetime.datetime.strptime(from_date, '%Y-%m-%d')
while date_now >= datetime.datetime.strptime(TO_DATE, '%Y-%m-%d'):
    print('Scraping papers from %s' % str(date_now.date()))

    # Query papers of this date
    try:
        papers = br.query('limit_from%%3A%s limit_to%%3A%s' % (str(date_now.date()),
                                                               str(date_now.date())),
                          full_text=False)

        # Extract words
        current_size = len(word_library)
        for i in range(len(papers)):
            new_words = word_cleanup(papers[i]['abstract'].split())
            word_library = word_library | new_words

        # Print result
        print('\nAdded %d new words to library of %d words' % (len(word_library) - current_size,
                                                               len(word_library)))

        # Save to disk
        file_library = open('word_library.obj', 'wb')
        pickle.dump(word_library, file_library)
        file_library.close()

        # Continue with day before
        date_now = date_now - datetime.timedelta(1)

    except Exception as error_message:
        print(error_message)
        error_log = open('error_log.txt', 'a')
        error_log.write('\n%s\n%s\n' % (datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),
                                        error_message))
        error_log.close()
