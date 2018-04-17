"""
    Index module for IR system

    Use the function run to load (or build) index file and print metadata.

"""

from future.utils import iteritems
from retrieve_data import *
import os
import pickle
import nltk
from nltk.corpus import stopwords
import pprint
import sys
from nltk.stem import WordNetLemmatizer


wordnet_lemmatizer = WordNetLemmatizer()


def _addToIndex(dataIndex, word, field, docId, pos):
    """ Add word to index

    Arguments:

        (inout) dataIndex: the index (dict)  
        word: word to add 
        field: field where the word was found
        docId: id of the document
        pos: position in the field

    """
    try:
        wordInfo = dataIndex[word]
    except KeyError:
        wordInfo = {}
    try:
        fieldInfo = wordInfo[field]
    except KeyError:
        fieldInfo = {}
    try:
        docInfo = fieldInfo[docId]
    except KeyError:
        docInfo = []
    docInfo.append(pos)
    fieldInfo[docId] = docInfo
    wordInfo[field] = fieldInfo
    dataIndex[word] = wordInfo


def addToIndex(dataIndex, word, field, docId, pos):
    """ Add word and its derivatives to index

    Arguments:

        (inout) dataIndex: the index (dict)  
        word: word to add 
        field: field where the word was found
        docId: id of the document
        pos: position in the field

    """
    w = word.lower()
    _addToIndex(dataIndex, word, field, docId, pos)
    # lemmatization
    lemma = wordnet_lemmatizer.lemmatize(w)
    if lemma != w:
        _addToIndex(dataIndex, lemma, field, docId, pos)


def index(data):
    """ Builds the index from input data.

    Argument:

        List of documents

    Returns:

        dict of word -> dict of field -> dict of docId -> list of positions. 

    """
    special = list(u',.;:()[]$%^@!*{}+=&<>/"\'')
    dataIndex = {}
    docId = 0
    for line in data:
        for field in line.keys():
            string = line[field]
            tokens = tokenizeField(line[field])
            pos = 0
            for word in tokens:
                if word not in special:
                    w = word.lower()
                    addToIndex(dataIndex, w, field, docId, pos)
                pos += 1
        docId += 1  
    return dataIndex            

def printIndexMeta(dataIndex):
    """ Print a summary of the index """
    print("Number of words indexed: %d."%(len(dataIndex)))

def countFun(dataIndex, word):
    """ Count the number of occurences of a word.

    Return:
        count 
    """

    if word not in dataIndex:
        return 0
    wordInfo = dataIndex[word]
    cnt = 0
    for field, fieldInfo in iteritems(wordInfo):
        for docId, docInfo in iteritems(fieldInfo): 
            cnt += len(docInfo)
    return cnt


def printIndexDebug(dataIndex):
    """ Print index debug information. """
    words = [key for key in dataIndex.keys() if len(key)>2] 
    histogram  = sorted(words, key=lambda w: -countFun(dataIndex,w))
    print("==Histogram==")
    for i in range(len(histogram)):
        print("%s: %d ocurrence(s)."%(histogram[i].encode('utf-8'),countFun(dataIndex,histogram[i])))
    
def createOrLoadIndex(data):
    """ Load (build) the index from the list of documents"""
    try:
        print("Load index...")
        dataIndex = loadIndex()
    except IOError:
        print("Build index...")
        dataIndex = index(data)
        pickle.dump( dataIndex , open( indexFile, "wb" ) )
    return dataIndex

def loadIndex():
    """ Load index from local file"""
    if os.path.isfile(indexFile):
        dataIndex = pickle.load( open( indexFile, "rb" ) )
    else:
        raise IOError("Index file does not exists!")
    return dataIndex

def test():
    """Basic testing of module"""
    print("Testing Index...")
    deleteFiles([indexFile])
    data = loadData()
    dataIndex = run(data)
    printIndexDebug(dataIndex)

def run(data):
    dataIndex = createOrLoadIndex(data)
    printIndexMeta(dataIndex)
    return dataIndex


def tokenizeField(s):
    """ Tokenize a field  """
    special = list('@=+-#%&*[]{}()?/"\';.,')
    stop = stopwords.words("english")
    s = s.replace('-',' - ');
    lst = nltk.word_tokenize(s)
    return [w for w in lst if w not in stop and w not in special]


if __name__ == "__main__":
    test()