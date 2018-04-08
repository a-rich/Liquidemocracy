import os
import sys
import json
from time import time
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

# Load in the document term matrix of the training data
if os.path.exists('document_term_matrix.pkl'):
    dtm = joblib.load('document_term_matrix.pkl')
else:
    print('This script must be run in a directory with a pickled document term matrix.')
    sys.exit()

# Load in the lables for the training data
if os.path.exists('labels.json'):
    y = json.load(open('labels.json', 'r'))
else:
    print('This script must be run in a directory with a labels file.')
    sys.exit()

# Create train/test split for X and y
X_train, X_test, y_train, y_test = train_test_split(
        dtm, y, test_size=0.33, random_state=42)

"""
        ('K-Nearest Neighbors', KNeighborsClassifier(n_neighbors=3)),
        ('Naive Bayes', MultinomialNB(alpha=0.05)),
"""
classifiers = [
        ('Support Vector Machine (Linear)', LinearSVC())
    ]

for model_name, clf in classifiers:
    start = time()
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    print('Took {} seconds to train and predict using {}'.format(time() - start, model_name))
    report = classification_report(y_test, predictions)
    print(report)
    #with open('reports.txt', 'a') as f:
     #   f.write('############### {} ###############\n{}\n{}\n'.format(model_name, clf.get_params(), report))
    #joblib.dump(clf, 'classifier.pkl')
