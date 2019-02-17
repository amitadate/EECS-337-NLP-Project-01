import json
import re
import nltk
from fuzzywuzzy import fuzz

def get_awards(year):
    extracted_text_data = get_tweets(year)
    def dataProcess(lawards):
        for (i,a) in enumerate(lawards):
            if "performance" not in a and ("actor" in a or "actress" in a) and "supporting" not in a:
                if "actor" in a:
                    lawards[i] = a.replace("actor","performance by an actor") 
                elif "actress" in a:
                    lawards[i] = a.replace("actress","performance by an actress") 
        return lawards

    def remove_duplicate(all_data, limit):
        for i in range(0, len(all_data)):
            for j in range(i+1, len(all_data)):
                if fuzz.ratio(all_data[i], all_data[j]) > limit or fuzz.token_set_ratio(all_data[i], all_data[j]) > limit or fuzz.token_sort_ratio(all_data[i], all_data[j]) > limit or fuzz.partial_ratio(all_data[i], all_data[j]) > limit:
                    all_data[j] = ""
        return list(set(all_data))

    awards = []
    pattern = re.compile(r'(?<=w[oi]n[s]\s)[Bb]est.*')
    tweet_sep = ['for','who',' s ','made',' | ', 'with' ,' at', ' http', ' #', '(','.', ',', '!', '?','\\', ':', ';', '"', "'",'the','but','although', 'made']
    awards_bag_of_words = ['-','performance', 'actress', 'actor', 'supporting', 'role', 'director', 'motion', 'picture', 'drama','animated', 'feature', 'film', 'song','comedy', 'musical', 'language', 'foreign','screenplay', 'orginal', 'television', 'tv', 'series', 'mini-series', 'mini']

    for tweet in extracted_text_data:
        award = re.findall(pattern, tweet)
        if award:
            for a in award:
                a = a.lower()
                for sep in tweet_sep:
                    if sep in a:
                        a = a.split(sep)[0]
                if "/" in a:
                    a = a.replace('/',' or ')
                awards.append(a)

    valid_awards = []
    for each in awards:
        each = each.lower()
        if len(set(each.split(" ")).intersection(set(awards_bag_of_words)))>2:
            valid_awards.append(each)
    
    valid_awards = [a[0] for a in nltk.FreqDist(valid_awards).most_common(5)]
    valid_awards.sort(key=lambda a: len(a),reverse=True)
    valid_awards = remove_duplicate(valid_awards, 95)
    valid_awards = dataProcess(valid_awards)

    retrun_list = []
    for each in valid_awards:
        if each == '':
            continue
        else:
            if "tv" in each:
                each = each.replace("tv", "television")
            retrun_list.append(each) 
    return retrun_list