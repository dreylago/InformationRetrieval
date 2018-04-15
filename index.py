"""
    Index module for IR system
"""
import urllib2
import gzip
import json
import os
import pickle

gzFile = './products.json.gz'
indexFile = './products.p'

def downloadData(url, dst):
    filedata = urllib2.urlopen(url)  
    data = filedata.read()
    with open(dst, 'wb') as f:  
        f.write(data)
        f.close()


def getRemoteData(url):
    if not os.path.isfile(gzFile):
        downloadData(url, gzFile)
        deleteFiles([indexFile])

def deleteFiles(files):
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

def loadData():
    with gzip.GzipFile(gzFile, 'r') as fin:
        data = json.loads(fin.read().decode('utf-8'))
        return data
    raise IOError("Error loading %s"%(gzFile))

def printDataMeta(data):
    """Shows meta-information of data"""
    print("%d elements."%(len(data)))
    print("Type of line0: %s." %(type(data[0])))
    print("Fields: %s." % (data[0].keys()))

def index(data):
    dataIndex = {}
    docId = 0
    for line in data:
        for field in line.keys():
            string = line[field]
            pos = 0
            for word in string.split():
                w = word.lower()
                info = (field, pos)
                try:
                    wordInfo = dataIndex[w]
                except KeyError:
                    wordInfo = {}
                try:
                    docInfo = wordInfo[docId]
                except KeyError:
                    docInfo = []
                docInfo.append(info)
                wordInfo[docId] = docInfo
                dataIndex[w] = wordInfo
                pos += 1
        docId += 1  
    return dataIndex            

def printIndexMeta(dataIndex):
    print("Number of Keys: %d."%(len(dataIndex)))

def countFun(wordInfo):
    cnt = 0
    for docId in wordInfo.keys():
        cnt += len(wordInfo[docId])
    return cnt

def histFun(dataIndex, word):
    if len(word)>4:
        return countFun(dataIndex[word])
    else:
        return 0

def printIndexDebug(dataIndex):
    histogram  = sorted(dataIndex.keys(), key=lambda w: -histFun(dataIndex,w))
    print("Histogram==")
    for i in range(20):
        print("%s: %d ocurrence(s)."%(histogram[i],countFun(dataIndex[histogram[i]])))
    

def createOrLoadIndex(data):
    try:
        print("Try load index...")
        dataIndex = loadIndex()
    except IOError:
        print("Build index...")
        dataIndex = index(data)
        pickle.dump( dataIndex , open( indexFile, "wb" ) )
    return dataIndex

def loadIndex():
    if os.path.isfile(indexFile):
        dataIndex = pickle.load( open( indexFile, "rb" ) )
    else:
        raise IOError("Index file does not exists!")
    return dataIndex

def test():
    """Basic testing of module"""
    print("Testing...")
    #deleteFiles([gzFile, indexFile])
    dataIndex = run()
    printIndexDebug(dataIndex)


def run():
    url = "https://s3-eu-west-1.amazonaws.com/pricesearcher-code-tests/software-engineer/products.json.gz"
    print("Get data...")
    getRemoteData(url)  
    data = loadData()  
    printDataMeta(data)
    print("Index data...")
    dataIndex = createOrLoadIndex(data)
    printIndexMeta(dataIndex)
    return dataIndex


if __name__ == "__main__":
    test()