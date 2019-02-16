def most_discussed(year,num=10):
    tweets = get_tweets(year)
    fashion_tweets = {}
    english_stop_words = set(stopwords.words('english'))
    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')
    for tweet in tweets:
        about_red_carpet = re.findall(r'on the red carpet|suit|dress|outfit|best dressed|worst dressed', tweet.lower())
        person_names = re.findall(name_pattern, tweet)
    
        if len(about_red_carpet) !=0 and len(person_names) !=0:
            for word in ["",'Golden Globes','Red Carpet','Best Dressed','Worst Dressed','Dressed List', 'Fashion Flops']:
                for name in person_names:
                    if word in name:
                        person_names.remove(name)
            for name in person_names:
                if name in fashion_tweets:
                    fashion_tweets[name] +=1
                else:
                    fashion_tweets[name] = 1

    for name in sorted(fashion_tweets, key=fashion_tweets.get, reverse=True)[:num]:
        print(name)


def best_dressed(year,num=9):
    tweets = get_tweets(year)
    fashion_tweets = {}
    english_stop_words = set(stopwords.words('english'))
    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')
    for tweet in tweets:
        about_red_carpet = re.findall(r'best dressed|best|loving|lovable|superb|fantastic|sexy|hot|stunning|love|stun|good|great|gorgeous|fab|fabulous|pretty|beutiful|awesome|handsome|amazing',tweet.lower())
        person_names = re.findall(name_pattern, tweet)
    
        if len(about_red_carpet) !=0 and len(person_names) !=0:
            for word in ["",'Golden Globes','Red Carpet','Best Dressed','Worst Dressed','Dressed List', 'Fashion Flops']:
                for name in person_names:
                    if word in name:
                        person_names.remove(name)
            for name in person_names:
                if name in fashion_tweets:
                    fashion_tweets[name] +=1
                else:
                    fashion_tweets[name] = 1

    for name in sorted(fashion_tweets, key=fashion_tweets.get, reverse=True)[:num]:
        print(name)

def worst_dressed(year,num=4):
    tweets = get_tweets(year)
    fashion_tweets = {}
    english_stop_words = set(stopwords.words('english'))
    name_pattern = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+')
    for tweet in tweets:
        
        about_red_carpet = re.findall(r'worst dressed|worst|hate|ugly|wtf|horribl| ew |hate|ugly| lack |bizarre|horrible|weird|out of place|too much|disgusting|trash|scandalous',tweet.lower())
        person_names = re.findall(name_pattern, tweet)
        if len(about_red_carpet) !=0 and len(person_names) !=0:
            for word in ["",'Golden Globes','Red Carpet','Best Dressed','Worst Dressed','Dressed List', 'Fashion Flops']:
                for name in person_names:
                    if word in name:
                        person_names.remove(name)
            for name in person_names:
                if name in fashion_tweets:
                    fashion_tweets[name] +=1
                else:
                    fashion_tweets[name] = 1

    for name in sorted(fashion_tweets, key=fashion_tweets.get, reverse=True)[:num]:
        print(name)
