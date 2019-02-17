def get_winner_new(year):

    award_list = OFFICIAL_AWARDS
    
    if not get_tweets(year):
        print("No data present")
        return None
    
    winners = {}
    for award in award_list:
        winners[award] = []
        
    tweet_award_dict = get_award_tweet_dict(year)

    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')
    award_list_person=[]
    for award in award_list:
        for person in ["actor","actress","demille","director"]:
            if person in award:
                award_list_person.append(award)
          
    for award in award_list_person:
        for tweet in tweet_award_dict[award]:
            names = re.findall(name_pattern, tweet)
            winners[award] = winners[award]+names
    freq={}
    for award in award_list_person:
        freq[award] = nltk.FreqDist(winners[award])
    
    # winner list for the rest
    award_list_not_person =[]
    for award in award_list:
        if award not in award_list_person:
            award_list_not_person.append(award)
                
    for award in award_list_not_person:
        ignore_list=["@","#"]
        winner_stoplist = ['-', 'animated', 'best', 'comedy', 'drama', 'feature', 'film', 'foreign', 'globe', 'goes', 'golden', 'motion', 'movie', 'musical', 'or', 'original', 'picture', 'rt', 'series', 'song', 'television', 'to', 'tv'] 
        bigrams_list = []
        ignore_list=["@","#"]
        
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


    for award in award_list:
        winners[award] = freq[award].most_common(1)[0][0]

    return winners
    
