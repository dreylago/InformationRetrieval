from future.utils import iteritems
import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()


def calcWeight(pos, field, onField):
    """ Calculate weight of matched word 

    Arguments:

        [int]  pos: position of word in the field
        [str]  field: field where the word was found
        [str]  onField: specific field to search for (title, merchant, description, all)

    Return:

        [float] weight 

    """

    weight = 0.
    # Assign weights according to field
    if field == u'title':
        # words in title weight more
        weight += 5. 
    elif field == u'merchant':
        weight += 1. 
    else:
        weight += 1. / (pos + 1.)

    # increase weight if onField is set and matches current field
    if field == onField:
        weight *= 2.

    return weight


def _weighWord(docs, dataIndex, word, onField=u"all", factor=1.0):
    """ Add a weight to documents that contain the word
    (helper function)

    Arguments:

        [dict] (inout) docs: dict of docId -> weight
        [dict] dataIndex: the index
        [str]  word: the word
        [str]  onField: specific field to search for (title, merchant, description, all)
        [float] factor: multiplicative factor

    Returns

        [bool] word was found in a document

    """

    if word not in dataIndex:
        return False

    wordInfo = dataIndex[word]

    for field, fieldInfo in iteritems(wordInfo):
        # skip if onField is not all and is different than current field
        if onField != u"all" and field != onField:
                continue

        for docId, docInfo in iteritems(fieldInfo):
            for pos in docInfo:
                weight = calcWeight(pos, field, onField) * factor
                if docId in docs:
                   docs[docId] += weight
                else:
                    docs[docId] = weight 

    return True

def weighWord(docs, dataIndex, word, onField=u"all"):
    """ Add a weight to documents that contain the word
    or its derivatives

    Arguments:

        (inout) docs: dict of docId -> weight
        dataIndex: the index
        word: the word
        onField: specific field to search for (title, merchant, description, all)

    """
    # exact word
    w = word.lower()
    _weighWord(docs, dataIndex, w, onField)
    # lemmatization
    lemma = wordnet_lemmatizer.lemmatize(w)
    # weigh the documents again with a damping factor
    _weighWord(docs, dataIndex, lemma, onField, 0.5)

def parseQuery(dataIndex, query):
    """ Naive query string parser.

    Arguments:
        [dict] dataIndex: the index
        [str] query: query 

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
    and/or logical operators (using recursive function).

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
            weighWord(docs, dataIndex, w, field)
    return docs


def tokenizeQuery(s):
    """ Tokenize a query string """
    special = list('@=+-#%&*[]{}()?/"\';.,')
    # temporary nltk fix 
    s = s.replace('-',' - ');
    lst = nltk.word_tokenize(s)
    return [w for w in lst if w not in special]