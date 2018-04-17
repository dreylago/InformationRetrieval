"""
    Print results module for IR system
"""
import time


def printDocs(data, docs, query):
    """ Print results 

    Arguments:

        [list] data: list of products
        [list] docs: list of docId, weights

    """ 

    print("%d document(s) found"%(len(docs)))
    descriptionMaxLen = 70
    pageSize = 3

    sep = ""
    i = 0
    ii = 1
    for _id, weight in docs:
        if i == pageSize:
            i = 0
            _input = raw_input("\n<<ENTER: continue (s+ENTER): save (q+ENTER): end search>> ")
            if _input == u"q":
                break   
            elif _input == u's':
                fn = saveSearch(data, docs, query)
                print("Search saved in file %s"%(fn)) 
                break         
        try:
            m = data[_id][u'merchant'].encode("utf-8")
            t = data[_id][u'title'].encode("utf-8")
            d = data[_id][u'description'].encode("utf-8")
            print("%s\n%d.-(%.2f) %s\nMerchant: %s\n%s."%(sep,ii,weight,t,m,d[:descriptionMaxLen]))
            sep = "=" * 70
            i += 1
            ii += 1
        except:
            print("Error accesing document %d"%(i))



def saveSearch(data, docs, query):
    """ Save results on file

    Arguments:

        [list] data: list of products
        [list] docs: list of docId, weights

    """

    filename = "saved-"+time.strftime("%Y%m%d-%H%M%S")+".txt"
    f = open(filename,'w')
    f.write("search > %s\n"%(query)) 
    f.write("%d document(s) found\n"%(len(docs)))
    sep = "=" * 70
    i = 0
    ii = 1
    for _id, weight in docs:         
        try:
            m = data[_id][u'merchant'].encode("utf-8")
            t = data[_id][u'title'].encode("utf-8")
            d = data[_id][u'description'].encode("utf-8")
            f.write("%s\n%d.-(%.2f) %s\nMerchant: %s\n%s.\n"%(sep,ii,weight,t,m,d))
            i += 1
            ii += 1
        except:
            print("Error accesing document %d"%(i))
    f.close()
    return filename



