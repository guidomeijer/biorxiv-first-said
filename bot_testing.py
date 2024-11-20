# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:24:04 2020

@author: Guido Meijer
"""

from atproto import Client

client = Client()
client.login('guido.meijer@donders.ru.nl', 'ToK78Wsvk!cV')
client.send_post(text='First test!')


"""
import pickle
from functions import word_cleanup
import datetime
from biorxiv_retriever import BiorxivRetriever
br = BiorxivRetriever()

# Load word library
word_library = pickle.load(open('word_library.obj', 'rb'))

# Scrape today's papers
today = datetime.date.today() - datetime.timedelta(days=1)
print('Scraping papers from %s' % str(today))
papers = br.query('limit_from%%3A%s limit_to%%3A%s' % (str(today), str(today)), full_text=False)

# Extract words
new_words = []
abstract_index = []
for i in range(len(papers)):
    these_words = word_cleanup(papers[i]['abstract'].split())
    for j, word in enumerate(these_words):
        if word not in word_library:
            new_words.append(word)
            abstract_index.append(i)
"""
