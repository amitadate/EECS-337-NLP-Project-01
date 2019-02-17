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

    tweet_award_dict = get_award_tweet_dict(year)
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

#         print(bigrams_list)

        freq[award] = nltk.FreqDist([' '.join(item) for item in bigrams_list])

    for award in award_list:
        #         print(award)
        #         print(freq[award].most_common(1)[0][0])
        winners[award] = freq[award].most_common(1)[0][0]

    return winners
