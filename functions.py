# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 15:30:19 2020

@author: Guido Meijer
"""

from string import punctuation


def remove_punctuation(value):
    punctuation_no_dash = punctuation + '“”‘’'
    punctuation_no_dash = punctuation_no_dash.replace('-', '')
    result = ""
    for c in value:
        if c not in punctuation_no_dash:
            result += c
    return result


def word_cleanup(word_list):
    clean_word_list = set()
    for word in word_list:
        clean_word = remove_punctuation(word)
        if (clean_word.islower() is False) or (any(map(str.isdigit, clean_word))):
            continue
        clean_word_list.add(clean_word)
    return clean_word_list
