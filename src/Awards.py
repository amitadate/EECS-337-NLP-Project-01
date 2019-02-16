import json
import re
import nltk
import copy
from fuzzywuzzy import fuzz

awards = []
pattern = re.compile(r'(?<=w[oi]n[s]\s)[Bb]est.*')
redlights = [' for','who',' s ','made',' | ', 'with' ,' at', ' http', ' #', '(','.', ',', '!', '?','\\', ':', ';', '"', "'",'the','but','although', 'made']
gender_award_words = ['-','Performance', 'performance', 'Actress', 'actress', 'Actor', 'actor', 'Supporting', 'supporting', 'Role', 'role', 'Director', 'director']
non_gender_award_words = ['Motion', 'motion', 'Picture', 'picture', '-', 'Drama', 'drama','Animated', 'animated', 'Feature', 'feature', 'Film', 'film', 'Foreign', 'Song', 'song','Comedy', 'comedy', 'Musical', 'musical', 'Language', 'language', 'foreign','Screenplay', 'screenplay', 'Original', 'orginal', 'Television', 'television', 'tv', 'Series', 'series', 'Mini-series',  'mini-series', 'mini', 'Mini']

def dataProcess(awards):
    for i in range(len(awards))[::-1]:
            award = awards[i].strip()
            for a in awards[:i]:
                if award in a.strip():
                    awards.pop(i)
                    break
    for (i,a) in enumerate(awards):
        if "tv" in a:
            awards[i] = a.replace("tv", "television")
    return awards

def remove_duplicate(all_data):
    limit = 85
    for i in range(0, len(all_data)):
        for j in range(i, len(all_data)):
            if fuzz.ratio(all_data[i], all_data[j]) > limit or fuzz.token_set_ratio(all_data[i], all_data[j]) > limit or fuzz.token_sort_ratio(all_data[i], all_data[j]) > limit or fuzz.partial_ratio(all_data[i], all_data[j]) > limit:
                try:
                    all_data.pop(j)
                    break
                except:
                    print("Error")
    return all_data

def getawards(extracted_text_data):
    for tweet in extracted_text_data:
        award = re.findall(pattern, tweet)
        if award:
            for a in award:
                a = a.lower()
                for light in redlights:
                    if light in a:
                        a = a.split(light)[0]
                if "/" in a:
                    a = a.replace('/',' or ')
                awards.append(a)
    #print(len(awards))

    update_gender_awards = []
    update_nonGender_awards = []
    for each in awards:
        each = each.lower()
        if len(set(each.split(" ")).intersection(set(gender_award_words)))>=2:
            update_gender_awards.append(each)
        if len(set(each.split(" ")).intersection(set(non_gender_award_words)))>3:
            if "actor" not in each and "actress" not in each:
                update_nonGender_awards.append(each)
    #print(len(update_gender_awards))
    #print(len(update_nonGender_awards))

    update_gender_awards.sort(key=lambda a: len(a),reverse=False)
    update_gender_awards = remove_duplicate(update_gender_awards)
    #print(len(update_gender_awards))

    update_gender_awards = [a[0] for a in nltk.FreqDist(update_gender_awards).most_common(50)]
    update_gender_awards.sort(key=lambda a: len(a),reverse=True)
    update_gender_awards = remove_duplicate(update_gender_awards)
    dataProcess(update_gender_awards)
    #print(len(update_gender_awards))


    update_nonGender_awards.sort(key=lambda a: len(a),reverse=False)
    update_nonGender_awards = remove_duplicate(update_nonGender_awards)
    #print(len(update_nonGender_awards))

    update_nonGender_awards = [a[0] for a in nltk.FreqDist(update_nonGender_awards).most_common(30)]
    update_nonGender_awards.sort(key=lambda a: len(a),reverse=True)
    update_gender_awards = remove_duplicate(update_gender_awards)

    dataProcess(update_nonGender_awards)
    #print(len(update_nonGender_awards))

    all_data = list(update_gender_awards) + list(update_nonGender_awards)
    print(all_data)
    return all_data