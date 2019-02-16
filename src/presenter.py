def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    ia = IMDb()
    if not get_tweets(year):
        print("No Data")
        return None
    award_tweet_dict = get_award_tweet_dict(year)

    presenters = {}
    stop = ["Award", "Film", "Movie", "Foreign"]

    p_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+(?=\spresent)')
    p2_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+\sand\s[A-Z][a-z]+\s[A-Z][a-z]+(?=\spresent|\sintroduc)')

    for award in award_tweet_dict:
        presenters[award] = []

        for tweet in award_tweet_dict[award]:
            presenter_pair = re.findall(p2_pattern, tweet)
            single_presenter = re.findall(p_pattern, tweet)
            flag = True

            for p in presenter_pair:
                p1 = p.split(' and')[0]
                if any(word in p1 for word in stop):
                    flag = False

                p2 = ' '.join((p.split(' and ')[1]).split(' ')[:2])
                if any(word in p2 for word in stop):
                    flag = False

                # first encounter of both presenters
                if flag:
                    person = ia.search_person(p1)
                    if person:
                        p1 = person[0]['name'].lower()
                    person = ia.search_person(p2)
                    if person:
                        p2 = person[0]['name'].lower()
                    if p1 not in presenters[award]:
                        presenters[award].append(p1)
                    if p2 not in presenters[award]:
                        presenters[award].append(p2)

            for p in single_presenter:
                if any(word in p for word in stop):
                    flag = False
                person = ia.search_person(p)
                if person:
                    p = person[0]['name'].lower()
                if flag and p not in presenters[award]:
                    presenters[award].append(p)

    return presenters
