import nltk
from nltk.corpus import stopwords
import re

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    tweets = get_tweets(year)
    stopword_list = stopwords.words('english')
    common_names = []
    for tweet in tweets:
        if re.findall(r"\s[hH]osted?",tweet):
            common_names.extend(nltk.bigrams(word for word in re.findall(r"['a-zA-Z]+\b",tweet) if word.lower() not in stopword_list))
    top = nltk.FreqDist(common_names).most_common(5)
    return [' '.join(top[0][0]), ' '.join(top[1][0])]


