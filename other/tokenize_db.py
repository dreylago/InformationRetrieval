from retrieve_data import * 
import nltk

data = loadData()  
for line in data:
    print("%s: %s.\n\n%s.\n===\n"%(line[u'merchant'].encode('utf-8'),line[u'title'].encode('utf-8'),line[u'description'].encode('utf-8')))
    mt = nltk.word_tokenize(line[u'merchant'])
    tt = nltk.word_tokenize(line[u'title'])
    dt = nltk.word_tokenize(line[u'description'])
    print("%s\n%s\n%s\n+++\n"%(mt,tt,dt))