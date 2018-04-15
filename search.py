"""
    Search module for IR system

    Naive command line interpreter to parse queries
    and return documents.

"""

from future.utils import iteritems
import os
import retrieve_data as rd
import index
import nltk
from nltk.corpus import stopwords
from print_docs import printDocs
from parse_query import parseQuery

def getDocLst(docs):
    """ Order list of documents and normalize weights.

    Arguments:
        docs: dict of docId -> weight

    Returns:
        ordered list of tuples (docId, weight)

    """

    # convert to list
    _docLst = []
    maxWeight = -1.
    for docId, weight in iteritems(docs):
        if weight > 0.:
            _docLst.append((docId, weight))
            if weight > maxWeight:
                maxWeight = weight

    # normalize weights
    docLst = []
    for docId, _weight in _docLst:
        weight = _weight
        if maxWeight > 0.1:
            weight = _weight / maxWeight
        docLst.append((docId, weight))

    # sort by weight
    return sorted(docLst, key=lambda x: -x[1])

def search(data, dataIndex, query):
    """ Execute search and print results.

    Arguments:
        data: list of documents.
        dataIndex: the index.
        query: string

    """

    _docs = parseQuery(dataIndex, query)
    docs = getDocLst(_docs)
    if len(docs)>0:
        printDocs(data, docs)
    else:
        print("Nothing found.")

def loop(data, dataIndex):
    """ Command line interpreter. 

    Arguments:
        data: list of documents.
        dataIndex: the index.

    The loop ends when the keyword :exit (or exit:)
    is entered.

    """

    while True:
        query = raw_input("\nsearch> ")
        if query.lower().strip() in ['q', 'q']:
            break;
        elif query:
            search(data, dataIndex, query)

def main():
    data = rd.loadData()
    dataIndex = index.run(data)
    loop(data, dataIndex)

if __name__ == "__main__":
    main()
    


