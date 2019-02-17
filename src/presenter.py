def get_presenters(year):
    ia = IMDb()
    if not get_tweets(year):
        print("No Data")
        return None
    award_tweet_dict = get_award_tweet_dict(year)

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

    return presenters_dict_by_awards
