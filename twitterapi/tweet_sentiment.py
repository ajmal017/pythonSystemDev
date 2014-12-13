import sys
import json
import re

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1]).readlines()
    tweet_file = open(sys.argv[2]).readlines()
    tweetlist = [json.loads(x) for x in tweet_file]
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    
    scores = {}
    for line in sent_file:
        word, score = line.split('\t')
        scores[word] = int(score)
        
    for i, tweet in enumerate(tweetlist):
        score = 0
        try:
            word_list = re.sub(r'[^\w\s]','',tweet['text']) \
                .strip().replace('\n',"").lower().split(' ')
                
            # print word_list
            for word in word_list:
                    if word in scores:
                        score += scores[word]
                        # print 'adding..', word, scores[word]
                
        except KeyError:
            pass

        print 'tweet', i, 'score', score

if __name__ == '__main__':
    main()
