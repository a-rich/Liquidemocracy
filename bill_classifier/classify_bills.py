import os
import re
import json
from sklearn.externals import joblib

def clean_text(text):
    return ' '.join([word for word in re.split(r'\s+', text)
                     if not re.search(r'(.)\1{2,}|[_\d\W]+', word)])

def classify_bills(bill_list):
    dtm = vec.transform([clean_text(b['text']) for b in bill_list])
    predictions = clf.predict(dtm)

    for i, prediction in enumerate(predictions):
        bill_list[i]['category'] = classes[str(prediction)]

    return bill_list

bills = json.load(open('../bill_collection/data.json', 'r'))
classes = json.load(open('class_mapping.json', 'r'))

vec = joblib.load('vector_space_model.pkl')
clf = joblib.load('classifier.pkl')

for level, _ in bills.items():
    if level == 'federal':
        bill_list = _
        bill_list = classify_bills(bill_list)
    else:
        for location, bill_list in _.items():
            bill_list = classify_bills(bill_list)

json.dump(bills, open('classified_bills.json', 'w'))
