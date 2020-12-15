# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:24:04 2020

@author: Guido Meijer
"""

import pickle
from functions import word_cleanup
import datetime
from biorxiv_retriever import BiorxivRetriever
br = BiorxivRetriever()

# Load word library
word_library = pickle.load(open('word_library.obj', 'rb'))

# Scrape today's papers
today = datetime.date.today()
print('Scraping papers from %s' % str(today))
papers = br.query('limit_from%%3A%s limit_to%%3A%s' % (str(today), str(today)), full_text=False)

# Extract words
new_words = set()
for i in range(len(papers)):
    these_words = word_cleanup(papers[i]['abstract'].split())
    for j, word in enumerate(these_words):
        if word not in word_library:
            print(word)
            new_words.add(word)
