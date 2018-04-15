from future.utils import iteritems
import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()


def _weightWord(docs, dataIndex, word, onField=u"all"):
    """ Add a weight to documents that contain the word

    Arguments:

        (inout) docs: dict of docId -> weight
        dataIndex: the index
        word: the word
        onField: if not none, search only on specified field (title, merchant, description, all)

    """

    if word not in dataIndex:
        return 

    wordInfo = dataIndex[word]

    for field, fieldInfo in iteritems(wordInfo):
        # skip if onField is not all and is different than current field
        if onField != u"all":
            if field != onField:
                continue

        for docId, docInfo in iteritems(fieldInfo):
            for pos in docInfo:
                weight = 0.
                # Assign weights according to field
                if field == u'title':
                    # words in title weight more
                    weight += 5.
                elif field == u'merchant':
                    weight += 1.
                else:
                    # words in description weight more
                    # if they are found earlier
                    weight += 1. / (pos + 1.)
                # increase weight if onField is set
                if field == onField:
                    weight += 10.
            if docId in docs:
                docs[docId] += weight
            else:
                docs[docId] = weight 

def weightWord(docs, dataIndex, word, onField=u"all"):
    """ Add a weight to documents that contain the word
    or its derivatives

    Arguments:

        (inout) docs: dict of docId -> weight
        dataIndex: the index
        word: the word
        onField: if not none, search only on specified field (title, merchant, description, all)

    """
    w = word.lower()
    _weightWord(docs, dataIndex, w, onField)
    w = wordnet_lemmatizer.lemmatize(w)
    _weightWord(docs, dataIndex, w, onField)


def parseQuery(dataIndex, query):
    """ Naive query string parser.

    Arguments:
        dataIndex: the index
        query: query string

    The query string is a list of words that will be searched in
    all fields. Example:

    > light bulb

    Field-specific searches are possible by using the field name
    (title, merchant, description) followed by a colon:

    > shirt merchant: lewis

    The word "shirt" will be searched on all fields. "lewis"
    and all words from there on will be searched only on merchant 
    field.

    To disable previous field name, use the keyword "all:"

    > merchant: lewis all: shirt

    In the future a proper query parser could be build enabling
    and/or logical operators (using reentrant functions).

    Returns:

        dict of docId -> weight

    """

    queryTokens = tokenizeQuery(query)

    docs = {}
    field = u"all"
    while True:
        if len(queryTokens)==0:
            break
        word = queryTokens.pop(0)
        next = ''
        if len(queryTokens)>0:
            next = queryTokens[0]
        w = word.lower()
        if w in [u'merchant',u'description',u'title',u'all'] and next == ':':
            field = w
        else:
            weightWord(docs, dataIndex, w, field)
    return docs


def tokenizeQuery(s):
    """ Tokenize a query string """
    special = list('@=+-#%&*[]{}()?/"\';.,')
    s = s.replace('-',' - ');
    lst = nltk.word_tokenize(s)
    return [w for w in lst if w not in special]