# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:38:33 2020

@author: guido
"""
import pickle
import sys

if len(sys.argv) != 2:
    print('You must input one word to be removed from the library')
else:
    word = sys.argv[1]

# Remove word from library
word_library = pickle.load(open('word_library.obj', 'rb'))
word_library.difference_update(set([word]))
file_library = open('word_library.obj', 'wb')
pickle.dump(word_library, file_library)
file_library.close()
