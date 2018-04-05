import re
import os
import sys
import json
import pandas as pd
import itertools
#from nltk.stem import WordNetLemmatizer, SnowballStemmer
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


def read_data(infile):
    data_json = json.load(open(infile, 'r'))
    classes = {k: i for i,k in enumerate(data_json.keys())}

    data = ((doc, classes[cls]) for cls, vals in data_json.items() for doc in vals)
    X_data, y_data = itertools.tee(data)
    X = list(zip(*X_data))[0]
    y = list(zip(*y_data))[1]

    return X, y, classes

def clean_data(docs):
    docs = list(docs)
    num_docs = len(docs)
    for i, doc in enumerate(list(docs)):
        new_doc = []
        for word in re.split(r'\s+', doc):
            if not re.search(r'(.)\1{2,}|[_\d\W]+', word):
                new_doc.append(word)
        docs[i] = ' '.join(new_doc)
        if i % 10000 == 0:
            print('Cleaning doc {} of {}'.format(i, num_docs))

    return docs


if __name__ == '__main__':

    """
    if os.path.exists('stemmed_data.json') and os.path.exists('labels.json'):
        docs = json.load(open('stemmed_data.json', 'r'))
        labels = json.load(open('labels.json', 'r'))
    else:
        if os.path.exists('cleaned_data.json') and os.path.exists('labels.json'):
            docs = json.load(open('cleaned_data.json', 'r'))
            labels = json.load(open('labels.json', 'r'))
        else:
            if len(sys.argv) > 1:
                infile = sys.argv[1]
            else:
                infile = 'data.json'

            docs, labels, classes = read_data(infile)
            docs = clean_data(docs)
            json.dump(docs, open('cleaned_data.json', 'w'))
            json.dump(labels, open('labels.json', 'w'))

        stemmer = SnowballStemmer('english')
        for i,doc in enumerate(list(docs)):
            stemmed = []
            for word in doc.split():
                stemmed.append(stemmer.stem(word))
            docs[i] = ' '.join(stemmed)

        json.dump(docs, open('stemmed_data.json', 'w'))

    lemmatizer = WordNetLemmatizer()
    analyzer = TfidfVectorizer().build_analyzer()

    def lemm_it(doc):
        return (lemmatizer.lemmatize(w) for w in analyzer(doc))

    vec = TfidfVectorizer(analyzer=lemm_it, strip_accents='unicode', stop_words='english')
    dtm = vec.fit_transform(docs)
    joblib.dump(vec, 'vector_space_model.pkl')
    joblib.dump(dtm, 'document_term_matrix.pkl')
    """
