
path = 'enwiki-20211020-pages-articles-multistream.xml'

import xml.etree.ElementTree as ET


def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


events = ("start", "end")
i = 0
title = None
for event, elem in ET.iterparse(path, events=events):
    tname = strip_tag_name(elem.tag)
    if event == 'end':
        if tname == 'title':
            title = elem.text
        if tname == 'text':
            contents = elem.text
        elif tname == 'page':
            print(title)
            print(contents)
            i+=1
            if(i == 0):
                exit()
            elem.clear()

print("Number of articles: ", i)
