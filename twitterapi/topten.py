#!/usr/bin/python
# topten.py

import sys
import json
import re
import operator

def loadFiles():
    tweet_file = open(sys.argv[1]).readlines()
    tweetlist = [json.loads(x) for x in tweet_file]
    return tweetlist

def count_hashtags(tweetlist):
    hashtags = {}
    for x in tweetlist:
        if 'entities' in x and x['entities']['hashtags'] != []:
            if x['entities']['hashtags'][0]['text'] in hashtags:
                hashtags[x['entities']['hashtags'][0]['text']] += 1
            else:
                hashtags[x['entities']['hashtags'][0]['text']] = 1
    return hashtags

if __name__ == "__main__":
    tweetlist = loadFiles()
    
    sorted_hashtags = sorted(count_hashtags(tweetlist).items(), 
                        key = operator.itemgetter(1), reverse=True)
    for i in range(0,10):
        print sorted_hashtags[i][0], sorted_hashtags[i][1]
