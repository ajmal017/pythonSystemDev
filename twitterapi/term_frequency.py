import sys
import json
import re
import enchant

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def get_wordlist(tweet):
    # Set Dictionary
    engDict = enchant.Dict('en_US')
        
    # get rid of special characters
    word_list = re.sub(r'[^\w\s]','',tweet['text'])
    # get rid of multiple spaces
    word_list = re.sub(' +',' ',word_list)
    # make into list of lowercase words
    word_list = word_list.strip().replace('\n',"").lower().split(' ')
    # remove ''
    word_list = [word for word in word_list 
                    if not (word == '' or is_number(word))]
    # strip words not in english dictionary
    if word_list != []: 
        try:
            word_list = [word for word in word_list 
                            if engDict.check(word)]
        except:
            print sys.exc_info(), word_list, h
    
    return word_list

def get_newscores(word_list):
    print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1]).readlines()
    tweet_file = open(sys.argv[2]).readlines()
    tweetlist = [json.loads(x) for x in tweet_file]
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    
    scores = {}
    sentiment_dict = {}
    
    for line in sent_file:
        word, score = line.split('\t')
        scores[word] = int(score)
        sentiment_dict[word] = {}
        sentiment_dict[word]['score'] = 0
        sentiment_dict[word]['count'] = 0
        
    #print sentiment_dict
    
    for h, tweet in enumerate(tweetlist):
        new_scores = {}
        try:
            word_list = get_wordlist(tweet)
            #print word_list
            
            for i, word in enumerate(word_list):
                
                if not word in sentiment_dict:
                    sentiment_dict[word] = {}
                    sentiment_dict[word]['count'] = 1
                    sentiment_dict[word]['score'] = 0
                else:
                    sentiment_dict[word]['count'] += 1
                    
                if word in scores:
                    sentiment_dict[word]['score'] += scores[word]
                    
                    # if first word, assign next
                    if i == 0 and len(word_list) > 1: 
                        if not word_list[i+1] in scores:
                            new_scores[word_list[i+1]] = scores[word]
                    #if last word, assign before
                    elif i == len(word_list) -1 and len(word_list) > 1: 
                        if not word_list[i-1] in scores and \
                                not word_list[i-1] in new_scores:
                            new_scores[word_list[i-1]] = scores[word]
                        elif not word_list[i-1] in scores and \
                                word_list[i-1] in new_scores:
                            new_scores[word_list[i-1]] += scores[word]
                    # if in between words
                    elif len(word_list) > 2:
                        #assign before
                        if not word_list[i-1] in scores and \
                                not word_list[i-1] in new_scores:
                            new_scores[word_list[i-1]] = scores[word]
                        elif not word_list[i-1] in scores and \
                                word_list[i-1] in new_scores:
                            new_scores[word_list[i-1]] += scores[word]
                        # assign after
                        if not word_list[i+1] in scores and \
                                not word_list[i+1] in new_scores:
                            new_scores[word_list[i+1]] = scores[word]
                        elif not word_list[i+1] in scores and \
                                word_list[i+1] in new_scores:
                            new_scores[word_list[i+1]] += scores[word]
                    #print 'scores dict', word, scores[word]  
                        
        except KeyError:
            pass
            
        """if not new_scores == {}:
            print h, word_list    
            print 'new scores', new_scores
        """
        
        for word in new_scores:
                sentiment_dict[word]['score'] += new_scores[word]
                #print word, new_scores[word]
                
    totalCount = sum([sentiment_dict[word]['count'] for word in sentiment_dict])
    #print 'total count', totalCount
                            
    for word in sentiment_dict:
        #print word, sentiment_dict[word]
        if sentiment_dict[word]['count'] != 0:
            sentiment_dict[word]['avg_score'] = \
                float(sentiment_dict[word]['score'] 
                        / sentiment_dict[word]['count'])
        else: 
            sentiment_dict[word]['avg_score'] = None
        
        sentiment_dict[word]['freq'] = \
            float(sentiment_dict[word]['count'] / totalCount)
        
        print word, sentiment_dict[word]
    

if __name__ == '__main__':
    main()
