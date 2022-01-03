import re
import pymongo
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

myclient = pymongo.MongoClient("mongodb://localhost:27017/")#Connect mongo client
mdb = myclient["Wiki-SE"]["Content"]
mdoc = myclient["Wiki-SE"]["Doc_info"]

term = 'himself'
term = PorterStemmer().stem(term)
term = term.lower()
arr = mdb.find_one({"S_Word":term})
print(arr['Tree'])
