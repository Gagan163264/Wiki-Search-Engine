import os
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import pymongo
#exit()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myclient.drop_database("Wiki-SE")
mdb = myclient["Wiki-SE"]["Content"]
mdoc = myclient["Wiki-SE"]["Doc_info"]

sourcepath = 'docs'

i = 1

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

def processpage(f):
    str = f.read()
    str = re.sub(r'\[\[([^\[]*?)\|\]\]', '\\1', str)
    str = str.split('[[')
    for page in str:
       if page == '':
           continue
       page  = page.split(']]')
       title = page[0]
       try:
           content = page[1]
       except:
           content += title
           continue
       if '\n' in title or len(title.split(' '))>15 or title.split(':', 1)[0]=='File':
           content += title
           continue
       title = re.sub('[^A-Za-z0-9\(\)\s-]+', '', title)
       if content.split(' ', 1)[0].strip().lower() == "#redirect":
           continue
       content = re.sub(r'=+', '', content)
       content = re.sub(r'\(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)\)', ' ', content)
       return title.replace(' ', '_'), content

#-----------------------------------------------------------------MAIN-------------------------------------------------
for filename in os.listdir(sourcepath):
    splitlines = ''
    with open(os.path.join(sourcepath + '/', filename), 'r', encoding = 'utf-8') as f:
        wcount = 0
        title, content = processpage(f)
        splitlines = content.split('.', 2)
        content = re.split(r'[\n\s\(\)-]', content)
        checked = 0
        index_shard = {}
        for word in content:
           if checked == 1:
               checked = 0
               neword = word.lower()
           else:
               neword = decontracted(re.sub(r'[^\w]*(\w.*?\w)[^\w]*[\s|\n]+', '\\1', word.lower()+' '))
               if ' ' in neword:
                   checked = 1
                   wlst = neword.split(' ')
                   content.insert(content.index(word)+1, wlst[1])
                   neword = wlst[0]
           if not neword.isalnum():
               continue
           stemmed = PorterStemmer().stem(neword)
           wcount+=1
           word_dict = {"Root":neword,"Doc_name":title, "Freq":1, "BM25_score":0}
           if stemmed in index_shard.keys():
               found = 0
               for indexdict in index_shard[stemmed]:
                   if indexdict['Doc_name'] == title and indexdict['Root']==neword:
                       indexdict['Freq']= indexdict['Freq']+1
                       found = 1
                       break
               if not found:
                   index_shard[stemmed].append(word_dict)
           else:
               index_shard[stemmed]=[word_dict]

        for word in index_shard.keys():
            for record in index_shard[word]:
                mdb.update_one({"S_Word":word}, {"$push":{"Tree":record}}, upsert=True)

        print(f"{i}) Page = ",filename, "title = ", title)
        len_var = len(splitlines)-1
        preview = ''
        if len_var <=0:
            preview = "Cant generate preview"
        else:
            for ite in range(len_var):
                preview += splitlines[ite]+'.'
            preview = preview.strip()

        Doc_info_dict = {"Title":title, "Length":wcount, "Preview":preview}
        mdoc.insert_one(Doc_info_dict)
        i+=1
        #if i == 2:
        #    exit()
