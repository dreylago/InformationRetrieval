"""
    Dumps IR database

"""

from retrieve_data import * 
import nltk

sep = ""
data = loadData()  
for line in data:
    m = line[u'merchant'].encode("utf-8")
    t = line[u'title'].encode("utf-8")
    d = line[u'description'].encode("utf-8")
    print("%s\n%s\nMerchant: %s\nDescription:\n%s."%(sep,t,m,d))
    sep = "=" * 70
