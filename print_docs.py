"""
    Print results module for IR system
"""


def printDocs(data, docs):
    
    descriptionMaxLen = 4000
    pageSize = 4

    sep = ""
    i = 0
    ii = 1
    for _id, weight in docs:
        if i == pageSize:
            i = 0
            _input = raw_input("\n<<Press Enter for more results. (q + Enter) to end this search>> ")
            if _input == u"q":
                break            
        try:
            m = data[_id][u'merchant'].encode("utf-8")
            t = data[_id][u'title'].encode("utf-8")
            d = data[_id][u'description'].encode("utf-8")
            print("%s\n%d.-%s\nMerchant: %s\n%s."%(sep,ii,t,m,d[:descriptionMaxLen]))
            sep = "=" * 70
            i += 1
            ii += 1
        except:
            print("Error accesing document %d"%(i))