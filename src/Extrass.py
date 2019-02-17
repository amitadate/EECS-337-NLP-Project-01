import nltk
nltk.download('words')
from nltk.corpus import words
import re
from PyDictionary import PyDictionary

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

def dressed(year,num=10):
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
    return best, worst, conterversial

def most_discussed(year,num=10):
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
    return return_names