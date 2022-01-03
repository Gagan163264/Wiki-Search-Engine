from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
import pymongo

def stopword(word):
    return False #Stopword detection function

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

myclient = pymongo.MongoClient("mongodb://localhost:27017/")#Connect mongo client
mdb = myclient["Wiki-SE"]["Content"]
mdoc = myclient["Wiki-SE"]["Doc_info"]

inpstr = input('Enter search: ')

inpstr = decontracted(inpstr) # remove contractions

inp =  re.split(r'[\n\s\(\)-]', inpstr) #split for every newline(\n), space(\s), -,  ( and )
# just split with space will also work if you cant do the above

search_terms = [] # Remove stopwords
for term in inp:
    if not stopword(term):
        search_terms.append(term.lower())#Convert to lower case

stemmed_seatch_terms = {} #create a new array for stemmed words in query
for term in search_terms:
    stemmed_seatch_terms[PorterStemmer().stem(term)]=term

Search_score_per_doc = {}

for term in stemmed_seatch_terms.keys():
    res = mdb.find({"S_Word":term})
    for word in res:
        if stemmed_seatch_terms[term] == word['Root']:
            multiplier = 2
        else:
            multiplier = 1
        if word['Doc_name'] in Search_score_per_doc.keys():
            Search_score_per_doc[word['Doc_name']]+=word['BM25_score']*multiplier #Add score to existing data
        else:
            Search_score_per_doc[word['Doc_name']]=word['BM25_score']*multiplier

#Sort dict by value and return
