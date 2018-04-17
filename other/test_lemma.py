import nltk
from nltk.stem import WordNetLemmatizer


def loop():
    wordnet_lemmatizer = WordNetLemmatizer()
    while True:
        query = raw_input("\nlemma > ")
        if query.lower().strip() in ['q']:
            break
        elif query:
            lemma = wordnet_lemmatizer.lemmatize(query)
            print("%s"%(lemma))


loop()