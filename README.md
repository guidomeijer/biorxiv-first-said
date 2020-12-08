# [bioRxiv first said](https://twitter.com/bioRxiv_first) 

A Twitter bot that crawls bioRxiv abstracts and tweets words that have never been used on bioRxiv before. Every day the script `bot.py` runs as a cron job from a Linux VPS server. The script crawls all abstracts published that day using the `biorxiv_retriever` package. The words from the abstracts are selected and cleaned up using the following criteria:
- Punctuation (excluding dashes) is stripped from the words
- Words with an upper-case letter are ignored to exclude acronyms
- Words with digits are ignored
- Words with <= 2 letters are ignored

The remaining words are checked against a library of words (`word_library.obj`) that I made by crawling all bioRxiv abstracts, extracting and cleaning up the words, and adding them to a Python set. New words are added to the library and tweeted one by one with a variable delay of max 2 hours between the tweets. Tweeting is done using the Python library for the Twitter API [Tweepy](https://www.tweepy.org/). If there are more than 5 new words that day the scripts randomly selects 5 words to tweet and saves the rest of the words in the backlog (`backlog_words.obj`). 

This project was heavily inspired by the Twitter bot New New York Times: [@NYT_first_said](https://twitter.com/NYT_first_said), [Github repo](https://github.com/MaxBittker/nyt-first-said)

