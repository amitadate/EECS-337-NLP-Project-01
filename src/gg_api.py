'''Version 0.35'''

######
import json
import re
from gender_detector.gender_detector import GenderDetector
from fuzzywuzzy import fuzz
from imdb import IMDb
import nltk
nltk.download('words')
from nltk.corpus import words
from nltk.corpus import stopwords
from PyDictionary import PyDictionary
import copy
###

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']



###
global OFFICIAL_AWARDS
OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315

global TWEETS
TWEETS = {}
TWEETS_AWARD ={}

global TWEETS_BY_AWARD_DICT
TWEETS_BY_AWARD_DICT = {}

###### global variables for JSON #######
global host_global
host_global = []
global presenters_global
presenters_global = {}
global nominee_global
nominee_global = {}
global winners_global
winners_global = {}
global m_disscussed
m_disscussed = []
global best_dressed_global
best_dressed_global = []
global worst_dressed_global
worst_dressed_global = []
global c_dressed_global
c_dressed_global =[]



def get_tweets(year):
    if year in TWEETS:
        return TWEETS[year]
    else:
        try:
            f = open('gg'+year+'.json')
            data = json.load(f)
            TWEETS[year] = [tweet['text'] for tweet in data]
            TWEETS_AWARD[year] = copy.deepcopy(TWEETS[year])
            divide_tweets(year)
            return TWEETS[year]
        except:
            return False


def get_tweet_by_award(year):
    if year in TWEETS_BY_AWARD_DICT:
        return TWEETS_BY_AWARD_DICT[year]
    else:
        divide_tweets(year)
        return TWEETS_BY_AWARD_DICT[year]


def divide_tweets(year):

    print("\nProcessing data of year {}".format(year))
    print("Might take under 4 minutes for 2013 and 5-6 minutes for 2015 ")

    tweets = get_tweets(year)
    tweet_by_award_dict = dict()

    for award in OFFICIAL_AWARDS:
        tweet_by_award_dict[award] = []

    to_delete = ['-', 'a', 'an', 'award', 'best', 'by', 'for', 'in', 'made', 'or', 'performance', 'role', 'feature', 'language']

    fresh_names = dict()
    for award in OFFICIAL_AWARDS:
        fresh_names[award] = [[item for item in award.split() if not item in to_delete]]

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
    TWEETS_BY_AWARD_DICT[year] = tweet_by_award_dict
    return



######


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
#########
def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    tweets = get_tweets(year)
    stopword_list = stopwords.words('english')
    stopword_list = stopword_list + ['#','?', 'golden', 'globe', 'globes', 'http', 'https', 'co']
    common_names = []
    for tweet in tweets:
        if re.findall(r"\s[hH]osted?",tweet):
            common_names.extend(nltk.bigrams(word for word in re.findall(r"['a-zA-Z]+\b",tweet) if word.lower() not in stopword_list))
    top = nltk.FreqDist(common_names).most_common(5)

    global host_global
    host_global = [' '.join(top[0][0]), ' '.join(top[1][0])]
    return [' '.join(top[0][0]), ' '.join(top[1][0])]
#########

def get_awards(year):
    get_tweet_by_award(year)
    extracted_text_data = TWEETS_AWARD[year]
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
    tweet_sep = ['for','who',' s ','made','yet','?', 'golden', 'globe', 'globes',' | ', 'with' ,' at', ' http', ' #', '(','.', ',', '!', '?','\\', ':', ';', '"', "'",'the','but','although', 'made']
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

    valid_awards = [a[0] for a in nltk.FreqDist(valid_awards).most_common(150)]
    valid_awards.sort(key=lambda a: len(a),reverse=True)
    valid_awards = remove_duplicate(valid_awards, 90)
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

#########
def get_nominees(year):
    ia = IMDb()

    if not get_tweets(year):
        print("No Data")
        return None

    stop_list_people = ['best','-','award','for','or','made', 'in', 'a', 'by', 'performance', 'an','golden','globes','role','motion','picture','best','supporting']
    nominees = {}
    nominee_names = {}
    cfd = {}
    detector = GenderDetector('us')
    award_list_person=[]
    freq={}
    award_list_not_person =[]


    for award in OFFICIAL_AWARDS:
        nominees[award] = []
        nominee_names[award]=[]

    tweet_award_dict = get_tweet_by_award(year)

    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')

    for award in OFFICIAL_AWARDS:
        for person in ["actor","actress","demille","director"]:
            if person in award:
                award_list_person.append(award)

    for award in award_list_person:
        for tweet in tweet_award_dict[award]:
            names = re.findall(name_pattern, tweet)
            for name in names:
                nominee_names[award].append(name)

    for award in award_list_person:

        if 'actor' in award:
            cfd[award] = nltk.FreqDist(nominee_names[award])
            most_common = cfd[award].most_common(50)
            for name in most_common:
                gender = detector.guess(name[0].split()[0])
                if gender == 'male':
                    p1 = name[0]
                    person = ia.search_person(p1)
                    if person:
                        p1 = person[0]['name'].lower()
                        if p1 not in nominees[award]:
                            nominees[award].append(p1)

        elif 'actress' in award:
            cfd[award] = nltk.FreqDist(nominee_names[award])
            most_common = cfd[award].most_common(50)
            for name in most_common:
                gender = detector.guess(name[0].split()[0])
                if gender == 'female':
                    p1 = name[0]
                    person = ia.search_person(p1)
                    if person:
                        p1 = person[0]['name'].lower()
                        if p1 not in nominees[award]:
                            nominees[award].append(p1)

        elif 'demille' in award:
            cfd[award] = nltk.FreqDist(nominee_names[award])
            most_common = cfd[award].most_common(50)
            for name in most_common:
                gender = detector.guess(name[0].split()[0])
                if gender != 'unknown':
                    p1 = name[0]
                    person = ia.search_person(p1)
                    if person:
                        p1 = person[0]['name'].lower()
                        if p1 not in nominees[award]:
                            if len(nominees[award]) <= 1:
                                nominees[award].append(p1)

        elif 'director' in award:
            cfd[award] = nltk.FreqDist(nominee_names[award])
            most_common = cfd[award].most_common(50)
            for name in most_common:
                gender = detector.guess(name[0].split()[0])
                if gender != 'unknown':
                    p1 = name[0]
                    person = ia.search_person(p1)
                    if person:
                        p1 = person[0]['name'].lower()
                        if p1 not in nominees[award]:
                            nominees[award].append(p1)


    for award in OFFICIAL_AWARDS:
        if award not in award_list_person:
            award_list_not_person.append(award)

    for award in award_list_not_person:
        ignore_list=["@","#"]
        winner_stoplist = ['Motion','Picture','Best','Supporting','-', 'animated', 'best', 'comedy', 'drama', 'feature', 'film', 'foreign', 'globe', 'goes', 'golden', 'motion', 'movie', 'musical', 'or', 'original', 'picture', 'rt', 'series', 'song', 'television', 'to', 'tv']
        bigrams_list = []


        for tweet in tweet_award_dict[award]:

            tweet = re.sub(r'[^\w\s]','',tweet)
            if tweet[0] == "R" and tweet[1]=="T":
                continue

            bigram = nltk.bigrams(tweet.split())

            temp=[]
            for item in bigram:
                if item[0].lower() not in winner_stoplist and item[1].lower() not in winner_stoplist:
                    temp.append(item)


            for item in temp:
                if item[0][0] not in ignore_list and item[1][0] not in ignore_list:
                    bigrams_list.append(item)


        freq[award] = nltk.FreqDist([' '.join(item) for item in bigrams_list])

    for award in award_list_not_person:
        most_common = freq[award].most_common(10)
        for name in most_common:
            p2 = name[0].lower()
            if p2 not in nominees[award]:
                nominees[award].append(p2)

    for k,v in nominees.items():
        if v:
            v.pop(0)



    global nominee_global
    nominee_global = nominees
    return nominees

#########
def get_winner(year):

    #award_list = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    award_list = OFFICIAL_AWARDS
    stop_list_people = ['best', '-', 'award', 'for', 'or', 'made', 'in', 'a', 'by', 'performance', 'an', 'golden', 'globes', 'role', 'motion', 'picture', 'best', 'supporting']
    #stop_list_people =['Motion Picture','Best Actor','Best Supporting']
    if not get_tweets(year):
        print("No Data")
        return None

    winners = {}
    for award in award_list:
        winners[award] = []

    tweet_award_dict = get_tweet_by_award(year)
    # print(tweet_award_dict)

    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')
    award_list_person = []
    for award in award_list:
        for person in ["actor", "actress", "demille", "director"]:
            if person in award:
                award_list_person.append(award)

    for award in award_list_person:
        for tweet in tweet_award_dict[award]:
            names = re.findall(name_pattern, tweet)
            for name in names:
                flag = False
                for name_item in name.lower().split():
                    if name_item in stop_list_people:
                        flag = True
                if flag == False:
                    winners[award] = winners[award] + [name]

    freq = {}
    for award in award_list_person:
        freq[award] = nltk.FreqDist(winners[award])

    # winner list for the rest
    award_list_not_person = []
    for award in award_list:
        if award not in award_list_person:
            award_list_not_person.append(award)

    for award in award_list_not_person:
        ignore_list = ["@", "#"]
        winner_stoplist = ['Motion', 'Picture', 'Best', 'Supporting', '-', 'animated', 'best', 'comedy', 'drama', 'feature', 'film', 'foreign', 'globe', 'goes', 'golden', 'motion', 'movie', 'musical', 'or', 'original', 'picture', 'rt', 'series', 'song', 'television', 'to', 'tv']
        bigrams_list = []
        ignore_list = ["@", "#"]

        for tweet in tweet_award_dict[award]:

            tweet = re.sub(r'[^\w\s]', '', tweet)
            if tweet[0] == "R" and tweet[1] == "T":
                continue

            bigram = nltk.bigrams(tweet.split())

            temp = []
            for item in bigram:
                if item[0].lower() not in winner_stoplist and item[1].lower() not in winner_stoplist:
                    temp.append(item)

            for item in temp:
                if item[0][0] not in ignore_list and item[1][0] not in ignore_list:
                    bigrams_list.append(item)

#        print(bigrams_list)

        freq[award] = nltk.FreqDist([' '.join(item) for item in bigrams_list])

    for award in award_list:
        #         print(award)
        #         print(freq[award].most_common(1)[0][0])
        winners[award] = freq[award].most_common(1)[0][0]

    global winners_global
    winners_global = winners

    return winners


#########
def get_presenters(year):
    #code for presenters
    ia = IMDb()
    if not get_tweets(year):
        print("No Data")
        return None
    award_tweet_dict = get_tweet_by_award(year)

    presenters_dict_by_awards = {}
    stop = ["Movie", "Foreign", "Golden", "Award", "GoldenGlobes", "Globes", "Goldenglobes", "Film"]

    single_presenter_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+(?=\spresent)')
    multiple_presenters_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+\sand\s[A-Z][a-z]+\s[A-Z][a-z]+(?=\spresent|\sintroduc)')

    for award in award_tweet_dict:
        presenters_dict_by_awards[award] = []

        for tweet in award_tweet_dict[award]:
            multiple_presenters = re.findall(multiple_presenters_pattern, tweet)

            for presenter in multiple_presenters:
                pp = presenter.split(' and ')
                p1 = pp[0]
                if any(word in p1 for word in stop):
                    continue

                pp = presenter.split(' and ')
                pt = pp[1]
                ptt = pt.split(' ')
                pttname = ptt[0:2]
                p2 = ' '.join(pttname)
                if any(word in p2 for word in stop):
                    continue

                person = ia.search_person(p1)
                if person:
                    p1 = person[0]['name'].lower()
                person = ia.search_person(p2)
                if person:
                    p2 = person[0]['name'].lower()
                if p1 not in presenters_dict_by_awards[award]:
                    presenters_dict_by_awards[award].append(p1)
                if p2 not in presenters_dict_by_awards[award]:
                    presenters_dict_by_awards[award].append(p2)

            single_presenter = re.findall(single_presenter_pattern, tweet)
            for presenter in single_presenter:
                if any(word in presenter for word in stop):
                    continue
                person = ia.search_person(presenter)
                if person:
                    presenter = person[0]['name'].lower()
                if presenter not in presenters_dict_by_awards[award]:
                    presenters_dict_by_awards[award].append(presenter)
    global presenters_global
    presenters_global = presenters_dict_by_awards
    return presenters_dict_by_awards

#########
def check_if_dict_word(word):
    swords = ["ew", "wtf", "def", "cumberbatch", "omg"]
    if "\n" in word:
        word = word.replace("\n", " ")
    for each in word.split(" "):
        if each[-1] == 's':
            each = each[0:len(each)-1]
        if each.lower() in words.words() or each.lower() in swords:
            return False
        else:
            continue
    return True

def dressed(year):
    num = 5
    tweets = get_tweets(year)
    fashion_best = {}
    fashion_worst = {}
    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')
    for tweet in tweets:
        best_dressed_regex = re.findall(r'best dressed|loving|lovable|superb|fantastic|sexy|hot|stunning|stun|good|great|gorgeous|fab|fabulous|pretty|beutiful|awesome|handsome|amazing',tweet.lower())
        worst_dressed_regex = re.findall(r'worst dressed|ugly|wtf|horribl| ew | lack |bizarre|horrible|weird|disgusting|trash|scandalous',tweet.lower())

        person_names = re.findall(name_pattern, tweet)
        if len(best_dressed_regex) !=0 and len(person_names) !=0:
            for name in person_names:
                if name in fashion_best:
                    fashion_best[name] +=1
                else:
                    fashion_best[name] = 1

        if len(worst_dressed_regex) !=0 and len(person_names) !=0:
            for name in person_names:
                if name in fashion_worst:
                    fashion_worst[name] +=1
                else:
                    fashion_worst[name] = 1

    best_names = sorted(fashion_best, key=fashion_best.get, reverse=True)
    worst_names = sorted(fashion_worst, key=fashion_worst.get, reverse=True)
    contervertial_names = []
    for b in range(0,len(best_names)-1):
        for w in range(0, len(worst_names)-1):
            if best_names[b] == worst_names[w]:
                contervertial_names.append(best_names[b])
                best_names[b] = ""
                worst_names[w] = ""

    best = []
    worst = []
    conterversial = []
    for name in best_names:
        if name == "":
            continue
        if len(best) == num:
            break
        if check_if_dict_word(name):
            best.append(name)
    for name in worst_names:
        if name == "":
            continue
        if len(worst) == num:
            break
        if check_if_dict_word(name):
            worst.append(name)
    for name in contervertial_names:
        if name == "":
            continue
        if len(conterversial) == num:
            break
        if check_if_dict_word(name):
            conterversial.append(name)

    global best_dressed_global
    global worst_dressed_global
    global c_dressed_global

    best_dressed_global = best
    worst_dressed_global = worst
    c_dressed_global = conterversial

    return best, worst, conterversial


#########
def most_discussed(year):
    num = 5
    tweets = get_tweets(year)
    fashion_tweets = {}
    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')
    for tweet in tweets:
        about_red_carpet = re.findall(r'on the red carpet|suit|dress|outfit|best dressed|worst dressed', tweet.lower())
        person_names = re.findall(name_pattern, tweet)

        if len(about_red_carpet) !=0 and len(person_names) !=0:
            for name in person_names:
                if name in fashion_tweets:
                    fashion_tweets[name] +=1
                else:
                    fashion_tweets[name] = 1
    all_names = sorted(fashion_tweets, key=fashion_tweets.get, reverse=True)
    return_names = []
    for name in all_names:
        if len(return_names) == num:
            break
        if check_if_dict_word(name):
            return_names.append(name)

    global m_disscussed
    m_disscussed = return_names

    return return_names

def set_official_awards(year):
    global OFFICIAL_AWARDS

    if str(year) in ['2013','2015']:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
        print("OFFICIAL LIST FOUND!!")

    elif str(year) in ['2018','2019']:
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
        print("OFFICIAL LIST FOUND!!")

    elif str(year).lower() == "exit":
        return


    else:
        print("KINDLY UPDATE OFFICIAL AWARD LIST PROVIDED, NOT IN YEAR 2013,2015,2018 or 2019")








#########
def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre Ceremony Proceesinng is Completed")
    return

def func_one(year):
    print ("\n Fetching Hosts for the Year ----> {}".format(year))
    hosts = get_hosts(year)
    print("\n")
    if len(hosts) == 2:
        print("\n The hosts for the year {} ----> {} ".format(year, " and ".join(hosts)))
        print("\n")
    print("\n")

def func_two(year):
    print("\n Fetching Awards for the Year ----> {}".format(year))
    awards = get_awards(year)
    print ("\nThe awards for {} are:\n".format(year))
    i = 0
    for award in awards:
        print (" {}. ----> {}".format(i+1,award))
        i = i +1
    print ("\n")

def func_three(year):
    print("\n Fetching Nominees for the Year ----> {}".format(year))
    nominees = get_nominees(year)
    print ("\nThe Nominees for {} are:\n".format(year))
    i = 0
    for award in nominees:
        print ('\n"{}. ----> {}"\n{}'.format(i+1,award, ", ".join(nominees[award])))
        i = i+1
        print("\n")
    print ("\n")

def func_four(year):
    print ("\nFetching Presenters for : {} ---->\n".format(year))
    presenters = get_presenters(year)
    i = 0

    for award in presenters:
        if len(presenters[award]) > 1:
            print ('{}. ----> The presenters for "{}" are {}.'.format(i+1,award, " and ".join(presenters[award])))
            i = i+1
        else:
            presenter = ("unknown")
            if len(presenters[award]) == 1:
                presenter = presenters[award][0]
            print ('{}. ----> The presenter for "{}" is {}.'.format(i+1,award, presenter))
            i = i+1
    print ("\n")

def func_five(year):
    print ("\nFetching winners for : {} ---->".format(year))
    winners = get_winner(year)
    print ("\nThe winners for :{} are:\n".format(year))
    i = 0
    for award in winners:
        print ('{}. ----> {}, for "{}"'.format(i+1,winners[award],award))
        i = i+1
    print ("\n")

def func_six(year):
    print ("\nGetting top 5 most discussed people on the red carpet for {}...".format(year))
    m = most_discussed(year)
    print ("\nThe top 5 most discussed people on the red carpet for {} are:\n".format(year))
    i = 0
    for name in m:
        print (" {}. ----> {}".format(i+1,name))
        i = i +1
    print ("\n")

def func_seven(year):
    print ("\nGetting top 5 CONTROVERSIALLY dressed people on the red carpet for {}...".format(year))
    list = []
    b,w,c = dressed(year)
    print ("\nThe top 5 CONTROVERSIALLY dressed people on the red carpet for {} are:".format(year))
    i =0
    for data in c:
        print ("\n")
        print (" {}. ----> {}".format(i+1,data))
        i = i +1
    print ("\n")


def func_eight(year):
    print ("\nGetting top 5 BEST dressed people on the red carpet for {}...".format(year))
    list = []
    b,w,c = dressed(year)
    print ("\nThe top 5 BEST dressed people on the red carpet for {} are:".format(year))
    i = 0
    for data in b:
        print ("\n")
        print (" {}. ----> {}".format(i+1,data))
        i = i +1
    print ("\n")

def func_nine(year):
    print ("\nGetting top 5 WORST dressed people on the red carpet for {}...".format(year))
    list = []
    b,w,c = dressed(year)
    print ("\nThe top 5 WORST dressed people on the red carpet for {} are:".format(year))
    i = 0
    for data in w:
        print ("\n")
        print (" {}. ----> {}".format(i+1,data))
        i = i +1
    print ("\n")


def get_json(year):
    global host_global
    global presenters_global
    global nominee_global
    global winners_global
    global m_disscussed
    global best_dressed_global
    global worst_dressed_global
    global c_dressed_global

    print("JSON FUNCION STARTED")

    if not host_global:
        get_hosts(year)

    if not presenters_global:
        get_presenters(year)

    if not nominee_global:
        get_nominees(year)

    if not winners_global:
        get_winner(year)

    if not m_disscussed:
        most_discussed(year)

    if not c_dressed_global:
        dressed(year)


    award = {}
    final = {"Host": host_global, "award_data":award}

    for key, value in winners_global.items():
       award[key] = dict()
       award[key]["nominees"] = nominee_global[key]
       award[key]["presenters"] = presenters_global[key]
       award[key]["winner"] = value

    with open('result'+year+'.json', 'w') as fp:
       json.dump(final, fp)

    print("JSON PUBLISHED")


    f = open('result'+year+'.txt', 'w')
    f.write("Host:"+",".join(host_global)+"\n")
    f.write("\n")
    for key, value in winners_global.items():
        f.write("Award:"+key+"\n")
        f.write("Presenters:"+",".join(presenters_global[key])+"\n")
        f.write("Nominees:"+",".join(nominee_global[key])+"\n")
        f.write("Winner:"+value+"\n")
        f.write("\n")

    f.write("Most Disscussed:"+",".join(m_disscussed)+"\n")
    f.write("Best Dressed:"+",".join(best_dressed_global)+"\n")
    f.write("Worst Dressed:"+",".join(worst_dressed_global)+"\n")
    f.write("Most Controversially Dressed:"+",".join(c_dressed_global)+"\n")
    f.close()


def default():
    print("\n KINDLY ENTER 1 - 9 or 0 to EXIT")



def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    pre_ceremony()

    year = ""
    while year != "exit":
        print ('\n\n\nTYPE EXIT TO QUIT PROGRAM.\nONLY VALID INPUTS ARE A YEAR NAME OR NUMBERS FROM [ 0 - 11]\nFOR OTHER INPUTS YOU WILL FACE AN ERROR \n\n\n *****KINDLY TYPE THE YEAR OF PREFERENCE***** \n\n ')
        print ('--------------------------------')
        year = input()
        set_official_awards(year)
        print ('--------------------------------')
        if year != "exit" :

            while True:
                print ('--------------------------------')
                print("CURRENT YEAR: {}".format(year))
                print ('--------------------------------')

                print("KINDLY CHOOSE FROM THE FOLLOWING CHOICES BELOW :")
                print ('--------------------------------')

                user_input = str(input("Enter 1 ----> Hosts\n\nEnter 2 ----> Awards\n\nEnter 3 ----> Nominees\n\nEnter 4 ----> Presenters\n\nEnter 5 ----> Winners\n\nEnter 6 ----> top 5 most discussed people\n\nEnter 7 ----> top 5 most controversially dressed\n\nEnter 8 ----> top 5 best dressed people\n\nEnter 9 ----> top 5 worst dressed people\n\nEnter 11 --> CREATE JSON FILE and TXT File\n\nEnter 0 ----> EXIT back to TOGGLE YEARS  "))

                if user_input == "0":
                    global host_global
                    host_global = []
                    global presenters_global
                    presenters_global = {}
                    global nominee_global
                    nominee_global = {}
                    global winners_global
                    winners_global = {}
                    global m_disscussed
                    m_disscussed = []
                    global best_dressed_global
                    best_dressed_global = []
                    global worst_dressed_global
                    worst_dressed_global = []
                    global c_dressed_global
                    c_dressed_global =[]
                    break
                else:
                    SWITCH_DICT = { "1" : func_one, "2" : func_two, "3" : func_three, "4" : func_four, "5" : func_five, "6" : func_six, "7" : func_seven, "8" : func_eight, "9" : func_nine, '11': get_json}
                    SWITCH_DICT[user_input](year)


    return

if __name__ == '__main__':
    main()
