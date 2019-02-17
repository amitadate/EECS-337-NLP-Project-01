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

    print("\nprocessing data for {} (this may take up to 7-8 minutes the first time)...".format(year))

    tweets = get_tweets(year)
    tweet_by_award_dict = dict()

    for award in OFFICIAL_AWARDS:
        tweet_by_award_dict[award] = []

    to_delete = ['-', 'a', 'an', 'award', 'best', 'by', 'for', 'in', 'made', 'or', 'performance', 'role', 'feature', 'language']

    fresh_names = dict()
    for award in OFFICIAL_AWARDS:
        fresh_names[award] = [[item for item in award.split() if not item in to_delete]]
#     print('####################FRESH NAMES##########################')
#     print(fresh_names)
#     print('#########################################################')

    for award in OFFICIAL_AWARDS:
        if "television" in award:
            extra = award.replace("television", 'tv')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("television", 't.v.')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

        if "motion picture" in award:
            extra = award.replace("motion picture", "movie")
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("motion picture", "film")
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

        if "film" in award:
            extra = award.replace("film", "motion picture")
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("film", "movie")
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

        if "comedy or musical" in award:
            extra = award.replace("comedy or musical", 'comedy')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("comedy or musical", 'musical')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

        if "series, mini-series or motion picture made for television" in award:
            extra = award.replace("series, mini-series or motion picture made for television", 'series')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("series, mini-series or motion picture made for television", 'mini-series')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("series, mini-series or motion picture made for television", 'miniseries')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("series, mini-series or motion picture made for television", 'tv')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("series, mini-series or motion picture made for television", 'television')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("series, mini-series or motion picture made for television", 'tv movie')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("series, mini-series or motion picture made for television", 'tv series')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("series, mini-series or motion picture made for television", 'television series')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

        if "mini-series or motion picture made for television" in award:
            extra = award.replace("mini-series or motion picture made for television", 'miniseries')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("mini-series or motion picture made for television", 'mini-series')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("mini-series or motion picture made for television", 'tv movie')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("mini-series or motion picture made for television", 'television movie')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

        if "television series" in award:
            extra = award.replace("television series", 'series')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("television series", 'tv')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("television series", 't.v.')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

            extra = award.replace("television series", 'television')
            fresh_names[award].append([item for item in extra.split() if not item in to_delete])

        if "television series - comedy or musical" in award:

            for word in ["tv comedy", "tv musical", "comedy series", "t.v. comedy", "t.v. musical", "television comedy", "television musical"]:
                extra = award.replace("television series - comedy or musical", word)
                fresh_names[award].append([item for item in extra.split() if not item in to_delete])

        if "television series - drama" in award:
            for word in ["tv drama", "drama series", "television drama", "t.v. drama"]:
                extra = award.replace("television series - drama", word)
                fresh_names[award].append([item for item in extra.split() if not item in to_delete])

    OFFICIAL_AWARDS.sort(key=lambda s: len(s), reverse=True)
#     print('####################FRESH NAMES##########################')
#     print(fresh_names)
#     print('#########################################################')
    for award in OFFICIAL_AWARDS:
        tweet_length = len(tweets)
        for i in range(tweet_length - 1, -1, -1):
            tweet = tweets[i]
            for extra in fresh_names[award]:
                flag = True
                for word in extra:
                    if flag == True:
                        flag = flag and word.lower() in tweet.lower()

                if flag == True:
                    tweet_by_award_dict[award].append(tweet)
                    del tweets[i]
                    break

#     for key in tweet_by_award_dict:
#         print(tweet_by_award_dict[key])
#         print(key)
#         break
    # cecil b. demille award
    #print(tweet_by_award_dict['cecil b. demille award'])
    # print('Called################')
    AWARD_TWEET_DICTS[year] = tweet_by_award_dict
    return
