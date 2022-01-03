import pymongo
import math

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mdb = myclient["Wiki-SE"]["Content"]
mdoc = myclient["Wiki-SE"]["Doc_info"]

k1 = 1.2
b = 0.75

avg = 0
t = 1
for document in mdoc.find():
    avg += (document["Length"]-avg)/t
    t+=1

t-=1
print("Average Doc length:",avg, t)
i = 0
for document in mdb.find():
    IDF = {}
    for elem in document['Tree']:
        if elem['Root'] in IDF.keys():
            if elem['Doc_name'] in IDF[elem['Root']].keys():
                IDF[elem['Root']][elem['Doc_name']]+=1
            else:
                IDF[elem['Root']][elem['Doc_name']]=1
        else:
            IDF[elem['Root']] = {elem['Doc_name']:1}
    record = []
    for elem in document['Tree']:
        fqi = len(IDF[elem['Root']])
        doclen = mdoc.find_one({'Title':elem['Doc_name']})['Length']
        wordfreq = int(elem['Freq'])#change
        IDF_val = math.log(1+((t-fqi+0.5)/(fqi+0.5)))
        elem['BM25_score']=IDF_val*((wordfreq*(k1+1))/(wordfreq+k1*(1-b+b*(doclen/t))))
        record.append(elem)
    mdb.update_one({"S_Word":document["S_Word"]}, {"$set":{"Tree":record}}, upsert=False)
    i+=1
    print(i, document['S_Word'])
