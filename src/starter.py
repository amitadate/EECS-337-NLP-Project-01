import json
import re
import nltk
from nltk.corpus import stopwords
from gender_detector.gender_detector import GenderDetector

#from gender_detector import GenderDetector
from string import punctuation
from imdb import IMDb
ia = IMDb()

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

global TWEETS
TWEETS = {}

global AWARD_TWEET_DICTS
AWARD_TWEET_DICTS = {}

def get_tweets(year):
    if year in TWEETS:
        return TWEETS[year]
    else:
        try:
            f = open('gg2013.json')
            data = json.load(f)
            TWEETS[year] = [tweet['text'] for tweet in data]
            sort_tweets(year)
            return TWEETS[year]
        except:
            return False

def get_award_tweet_dict(year):
    if year in AWARD_TWEET_DICTS:
        return AWARD_TWEET_DICTS[year]
    else:
        sort_tweets(year)
        return AWARD_TWEET_DICTS[year]
    
def sort_tweets(year):

    print ("\nprocessing data for {} (this may take up to 7-8 minutes the first time)...".format(year))

    tweets = get_tweets(year)
    print('what')
    award_tweet_dict = {award:[] for award in OFFICIAL_AWARDS}

    stoplist = ['best','-','award','for','or','made', 'in', 'a', 'by', 'performance', 'an','role']
    clean_award_names = {award:[[a for a in award.split() if not a in stoplist]] for award in OFFICIAL_AWARDS}
    #print(clean_award_names)


    substitutes = {}
    substitutes["television"] = ['tv','t.v.']
    substitutes["motion picture"] = ["movie", "film"]
    substitutes["film"] = ["motion picture", "movie"]
    substitutes["comedy or musical"] = ['comedy','musical']
    substitutes["series, mini-series or motion picture made for television"] = ['series','mini-series','miniseries','tv','television','tv movie','tv series', 'television series']

    substitutes["mini-series or motion picture made for television"] = ['miniseries','mini-series','tv movie','television movie']
    substitutes["television series"] = ['series','tv','t.v.','television']
    substitutes["television series - comedy or musical"] = ["tv comedy", "tv musical", "comedy series", "t.v. comedy", "t.v. musical", "television comedy", "television musical"]
    substitutes["television series - drama"] = ["tv drama", "drama series", "television drama", "t.v. drama"]
    substitutes["foreign language"] = ["foreign"]

    for award in OFFICIAL_AWARDS:
        for key in substitutes:
            if key in award:
                for sub in substitutes[key]:
                    alt_award = award.replace(key, sub)
                    clean_award_names[award].append([w for w in alt_award.split() if not w in stoplist])


    OFFICIAL_AWARDS.sort(key=lambda s: len(s), reverse=True)
    for award in OFFICIAL_AWARDS:
        # print "{} tweets unsorted".format(len(tweets))
        for i in range(len(tweets)-1,-1,-1):
            tweet = tweets[i]
            for alt_award in clean_award_names[award]:
                contains_important_words = True
                for word in alt_award:
                    contains_important_words = contains_important_words and word.lower() in tweet.lower()

                if contains_important_words:
                    # print alt_award
                    award_tweet_dict[award].append(tweet)
                    del tweets[i]
                    break

    AWARD_TWEET_DICTS[year] = award_tweet_dict
    return
