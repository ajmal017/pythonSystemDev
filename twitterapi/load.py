import sys
import json
import re
import enchant


engDict = enchant.Dict('en_US')
sent_file = open('AFINN-111.txt').readlines()
tweet_file = open('output.txt').readlines()
tweetlist = [json.loads(x) for x in tweet_file]
