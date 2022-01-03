from cleaner import *
from loader  import *
import os

if not os.path.exists('DB'):
    os.makedirs('DB')

path = 'enwiki-20211020-pages-articles-multistream.xml'
outpath = 'out.txt'
f = open(outpath, "w", encoding = "utf-8")

i = 0
cleaner = Cleaner()
for title, text in iterate(path):
    text = cleaner.clean_text(text)
    cleaned_text, links = cleaner.build_links(text)
    if cleaned_text.split(" ", 2)[0] == 'REDIRECT':
        continue
    print(text)
    print(title)
    #open('DB/'+title+'.txt', "w", encoding = "utf-8").write(cleaned_text)
    i+=1

print("Done:", i)
