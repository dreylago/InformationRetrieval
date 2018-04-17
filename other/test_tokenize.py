import nltk

def loop():
    while True:
        query = raw_input("\ntokenize > ")
        if query.lower().strip() in ['q']:
            break
        elif query:
            tokens = nltk.word_tokenize(query)
            print("%s"%(tokens))


loop()