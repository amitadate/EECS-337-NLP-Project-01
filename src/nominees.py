def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    if get_tweets(year) == False:
        return {}
    

    nominees = {}
    nominee_names = {}
    clean_award_names = {}
    stoplist = ['best','-','award','for','or','made', 'in', 'a', 'by', 'performance', 'an','golden','globes','role','the']
    cfd = {}
    detector = GenderDetector('us')
    
    for award in OFFICIAL_AWARDS: 
        nominees[award]=[]
        nominee_names[award]=[]
        clean_award_names[award] = [a for a in award.split() if not a in stoplist]

    person_award_identifiers = ["director","actor","actress","demille"]
    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')


    for award in OFFICIAL_AWARDS:
        if any(identifier in award for identifier in person_award_identifiers):
            for tweet in award_tweet_dict[award]:
                names = re.findall(name_pattern, tweet)
                for name in names:
                    award_not_in_name = True
                    for word in clean_award_names[award]+stoplist:
                        award_not_in_name = award_not_in_name and not word in name.lower().split()
                    if award_not_in_name:
                        nominee_names[award].append(name)

    
    for award in OFFICIAL_AWARDS:

        if 'actor' in award:
            cfd[award] = nltk.FreqDist(nominee_names[award])
            most_common = cfd[award].most_common(50)
            for name in most_common:
                gender = detector.guess(name[0].split()[0])
                if gender == 'male':
                    nominees[award].append(name[0])

        elif 'actress' in award:
            cfd[award] = nltk.FreqDist(nominee_names[award])
            most_common = cfd[award].most_common(50)
            for name in most_common:
                gender = detector.guess(name[0].split()[0])
                if gender == 'female':
                    nominees[award].append(name[0])

        elif any(identifier in award for identifier in ['director','demille']):
            cfd[award] = nltk.FreqDist(nominee_names[award])
            most_common = cfd[award].most_common(50)
            for name in most_common:
                gender = detector.guess(name[0].split()[0])
                if gender != 'unknown':
                    nominees[award].append(name[0])

        else:
            winner_stoplist = ["musical","comedy","motion", "picture","golden","globe","movie","television","best","or","tv","original","series","animated","feature","film","song","drama","-","rt","to","goes","foreign",'the']
            bigrams = []
            for tweet in award_tweet_dict[award]:
                if tweet[:2] == "RT":
                    continue
                tweet_bigrams = nltk.bigrams(tweet.split())
                trimmed = [b for b in tweet_bigrams if b[0].lower() not in winner_stoplist and b[1].lower() not in winner_stoplist and b[0][0] == b[0][0].upper()]
                bigrams += [b for b in trimmed if b[0][0] != "@" and b[1][0] != "@" and b[0][0] != "#" and b[1][0] != "#"]
            cfd[award] = nltk.FreqDist([' '.join(b) for b in bigrams])
            nominees[award] = [n[0] for n in cfd[award].most_common(5)]
        
    # nominees = {award: [a[0] for a in cfd[award].most_common(5)] for award in OFFICIAL_AWARDS}

    return nominees