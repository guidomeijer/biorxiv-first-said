# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 15:30:19 2020

@author: Guido Meijer
"""
from os.path import isfile


def remove_punctuation(word):
    punctuation = '.,()[]—–-;/?$&*:′‘’“”\'\"″'
    try:
        while word[0] in punctuation:
            word = word[1:]
        while word[-1] in punctuation:
            word = word[:-1]
    except:
        word = ''
    return word


def word_cleanup(word_list):
    punctuation = '.,()/;′’:\'\"{}'
    clean_word_list = set()
    for word in word_list:
        clean_word = remove_punctuation(word)
        if ((clean_word.islower() is True) and not (any(map(str.isdigit, clean_word)))
                and (clean_word.count('-') == 0) and (clean_word.count('–') == 0)
                and (any(elem in punctuation for elem in clean_word) is False)
                and (len(clean_word) > 3)):
            clean_word_list.add(clean_word)
    clean_word_list.difference_update([i for i in clean_word_list if i.startswith('http')])
    clean_word_list.difference_update([i for i in clean_word_list if i.startswith('www')])
    return clean_word_list


def context(content, word):
    """
    Function by Max Bittker (https://github.com/MaxBittker/nyt-first-said/)
    """
    loc = content.find(word)
    to_period = content[loc:].find('.')
    prev_period = content[:loc].rfind('.')
    allowance = 82
    if to_period < allowance:
        end = content[loc:loc + to_period + 1]
    else:
        end = u'{}…'.format(content[loc:loc + allowance])

    if loc - prev_period < allowance:
        start = u'{} '.format(content[prev_period + 2: loc].strip())
    else:
        start = u'…{}'.format(content[loc - allowance:loc])

    return u'{}{}'.format(start, end)


def init_log_files():
    LOG_FILES = ['log', 'library_update_log']
    for i, log in enumerate(LOG_FILES):
        if not isfile('%s.txt' % log):
            open('%s.txt' % log, 'a').close()
