import sys
import json
import re
import geocoder
import operator

def get_geo(loc_tweet):
    for x in loc_tweet:
        if 'place' in loc_tweet[x]:
            if not 'time_zone' in loc_tweet[x]:
                g = geocoder.google(loc_tweet[x]['coordinates'],method='reverse')
                print 'place without time_zone', \
                    loc_tweet[x]['place']['country'], \
                    loc_tweet[x]['coordinates'], \
                    g.address
                loc_tweet[x]['time_zone']= g.address
    
    return loc_tweet

def getTweetsWithLocationData(tweetlist):
    loc_tweet = {}
    for i, x in enumerate(tweetlist):
        try:
            
            if ('place' in x and x['place'] != None):
                if not str(i) in loc_tweet:
                    loc_tweet[str(i)] = {}
                loc_tweet[str(i)]['place'] = x['place']
                
            if ('coordinates' in x and x['coordinates'] != None):
                if not str(i) in loc_tweet:
                    loc_tweet[str(i)] = {}
                loc_tweet[str(i)]['coordinates'] \
                                    = x['coordinates']['coordinates']
                                    
            if ('user' in x and 'time_zone' in x['user'] 
                    and x['user']['time_zone'] != None):
                if not str(i) in loc_tweet:
                    loc_tweet[str(i)] = {}
                loc_tweet[str(i)]['time_zone'] = x['user']['time_zone']
                
            if ('user' in x and 'location' in x['user'] 
                    and x['user']['location'] != None 
                    and x['user']['location'] != '' ):
                if not str(i) in loc_tweet:
                    loc_tweet[str(i)] = {}
                loc_tweet[str(i)]['location'] = x['user']['location']
                
            if (str(i) in loc_tweet and 'text' in x and x['text'] != None):    
                loc_tweet[str(i)]['text'] = x['text']
            
        except:
            print sys.exc_info()
    
    # fill in missing locations
    for x in loc_tweet:
        if 'place' in loc_tweet[x] and not 'coordinates' in loc_tweet[x]:
            coords = loc_tweet[x]['place']['bounding_box']['coordinates']
            coords = str(coords).replace('[','').replace(']','').replace(' ','').split(',') 
            loc_tweet[x]['coordinates']= [float(coords[0]),float(coords[1])]
    
    # Get geolocation
    #get_geo(loc_tweet)        
    
    #  [place] seems to always have [place][coordinates]
    #  not all tweets with [place] has [coordinates]
    #  all tweets with [coordinates] has [place]
    #  add [coordinates] to tweets with [place] that do not have [coordinates]
    """for x in loc_tweet:
    if 'place' in loc_tweet[x]:
        if not 'country' in loc_tweet[x]['place']:
            print 'missing country'
        if not 'country_code' in loc_tweet[x]['place']:
            print 'missing code'
        if not 'name' in loc_tweet[x]['place']:
            print 'missing name'
        if not 'full_name' in loc_tweet[x]['place']:
            print 'missing full_name'
    """
    
    return loc_tweet

def getLocationScores(loc_tweet, sent_file):
    scores = {}
    loc_scores_bytimezone = {}
    loc_scores_byfullname = {}
    
    for line in sent_file:
        word, score = line.split('\t')
        scores[word] = int(score)

    for i,j in enumerate(loc_tweet):
        score = 0
        try:
            word_list = re.sub(r'[^\w\s]','',loc_tweet[j]['text']) \
                .strip().replace('\n',"").lower().split(' ')
                
            # print word_list
            for word in word_list:
                    if word in scores:
                        score += scores[word]
                        # print 'adding..', word, scores[word]
                
        except KeyError:
            pass

        if score != 0:
            if 'time_zone' in loc_tweet[j]:
                if loc_tweet[j]['time_zone'] in loc_scores_bytimezone:
                    loc_scores_bytimezone[loc_tweet[j]['time_zone']] += score
                else:
                    loc_scores_bytimezone[loc_tweet[j]['time_zone']] = score
            if 'place' in loc_tweet[j]:
                if loc_tweet[j]['place']['full_name'] in loc_scores_byfullname:
                    loc_scores_byfullname[loc_tweet[j]['place']['full_name']] += score
                else:
                    loc_scores_byfullname[loc_tweet[j]['place']['full_name']] = score
            """
            elif 'location' in loc_tweet[j]:
                if loc_tweet[j]['location'] in loc_scores:
                    loc_scores[loc_tweet[j]['location']] += score
                else:
                    loc_scores[loc_tweet[j]['location']] = score
             """       
        #print 'tweet', j, 'score', score, loc_tweet[j]
    loc_scores_bytimezone_sorted = sorted(loc_scores_bytimezone.items(), 
                        key = operator.itemgetter(1), reverse=True)
    loc_scores_byfullname_sorted = sorted(loc_scores_byfullname.items(), 
                        key = operator.itemgetter(1), reverse=True)
    return loc_scores_bytimezone_sorted, loc_scores_byfullname_sorted
    
def main():
    sent_file = open(sys.argv[1]).readlines()
    tweet_file = open(sys.argv[2]).readlines()
    tweetlist = [json.loads(x) for x in tweet_file]
    
    # get tweets with location data
    loc_tweet = getTweetsWithLocationData(tweetlist)
    # get scores by location
    scores_bytimezone, scores_byfullname = getLocationScores(loc_tweet,         sent_file)
    
    print "Top/Bottom 10 Sentiment Scores by Timezone\n"
    for i in range(0,10):
        print scores_bytimezone[i][0], scores_bytimezone[i][1], \
            scores_bytimezone[len(scores_bytimezone)-i-1][0], \
            scores_bytimezone[len(scores_bytimezone)-i-1][1]
            
    print "\n\nTop/Bottom 10 Sentiment Scores by City\n"
    for i in range(0,10):
        print scores_byfullname[i][0], scores_byfullname[i][1], \
            scores_byfullname[len(scores_byfullname)-i-1][0], \
            scores_byfullname[len(scores_byfullname)-i-1][1]

if __name__ == '__main__':
    main()
