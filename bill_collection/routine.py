import os
import json
import subprocess
from glob import glob
from mongoengine import connect
from liquidemocracy.models import *


##############################################################################
###             Run scrapers and aggregate data                            ###
##############################################################################

all_data = {
        'federal': [],
        'states': {},
        'counties': {},
        'cities': {}
        }

scrapers = glob('scrapers/**/scraper.py', recursive=True)

for scraper in scrapers:
    path_split = scraper.split('/')
    folder = '/'.join(path_split[:-1])
    scraper = path_split[-1]

    origWD = os.getcwd()
    os.chdir(folder)
    subprocess.call(['python3', scraper])
    os.chdir(origWD)

    data_file = folder + '/data.json'

    try:
        data = json.load(open(data_file, 'r'))
    except:
        print('No new data collected.')
        continue

    level = path_split[1]
    region = ''
    if level != 'federal':
        region = path_split[2]
        all_data[level][region] = data
    else:
        all_data[level] = data

    os.unlink(data_file)

json.dump(all_data, open('data.json', 'w'))


##############################################################################
###             Predict the policy area for all bills                      ###
##############################################################################


origWD = os.getcwd()
os.chdir('../bill_classifier')
subprocess.call(['python3', 'classify_bills.py'])
os.chdir(origWD)
os.unlink('data.json')


##############################################################################
###             Insert bills into the database                             ###
##############################################################################


def insert_bill(bill, location, level):
    if type(bill['authors']) is list:
        authors = ', '.join(bill['authors'])
    else:
        authors = bill['authors']
    Bill(
            title=bill['title'],
            category=bill['category'],
            date=bill['date'],
            authors=authors,
            text=bill['text'],
            source=bill['source'],
            vote_info=VoteInfo(),
            location=location,
            level=level
            ).save()

os.chdir('../bill_classifier')
bills = json.load(open('classified_bills.json', 'r'))

connect('liquidemocracy')

for level, _ in bills.items():
    if level == 'federal':
        bill_list = _
        for b in bill_list:
            insert_bill(b, Location(), level)
    else:
        for location, bill_list in _.items():
            city, county, state = '', '', ''

            if level == 'cities':
                city = location
            elif level == 'counties':
                county = location
            elif level == 'states':
                state = location

            for b in bill_list:
                location=Location(city=city, county=county, state=state)
                insert_bill(b, location, level)

os.unlink('classified_bills.json')
