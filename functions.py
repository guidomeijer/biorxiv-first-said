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
        if ((clean_word.islower() is True) and not (any(map(str.isdigit, clean_word)))
                and (clean_word[0] != '–') and (clean_word[-1] != '–')
                and (clean_word[0] != '-') and (clean_word[-1] != '-')
                and (clean_word.count('-') <= 1) and (clean_word.count('–') <= 1)
                and (len(clean_word) >= 2)):
            clean_word_list.add(clean_word)
    clean_word_list.difference_update([i for i in clean_word_list if i.startswith('http')])
    clean_word_list.difference_update([i for i in clean_word_list if i.startswith('www')])
    return clean_word_list
