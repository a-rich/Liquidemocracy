import json
import requests
import os
from dateutil import parser
from datetime import datetime
from bs4 import BeautifulSoup

class Scraper():
    web_page = None
    log = None
    manifest = None
    file_source_mape = {}

    def __init__(self, web_page):
        self.web_page = web_page
        self.log = open('exec.log', 'a')

        if os.path.exists('manifest.json'):
            self.manifest = json.load(open('manifest.json', 'r'))
        else:
            self.manifest = {}

    def fetch_docs(self):
        self.log.write('\n\n############################################################################\n')
        self.log.write('[{}]:  requesting from California state web page - {}'.format(
                datetime.now(), self.web_page))
        self.log.write('\n##############################################################################\n')

        print('*** Requestng from the California state web page ***\n')

        base_page = self.web_page + "/faces/dailyUpdates.xhtml?house="
        chambers = ['A', 'S']

        unprocessed_bills = []
        for chamber in chambers:

            bills_page = base_page + chamber

            self.log.write('[{}]:  requesting bills from chamber {}'.format(
                    datetime.now(), chamber))

            print('*** Request bills from the California state {} ***\n'.format(
                        'Assembly' if chamber == 'A' else 'Senate'))

            # Get a listing of all the current bills in the different chambers
            page = requests.get(bills_page)
            soup = BeautifulSoup(page.text, 'html.parser')
            bills = soup.find_all('td', {'class': 'billMeasureColClass'})
            bills = [next(b.descendants) for b in bills]
            bills = [(b.text, b.attrs['href']) for b in bills]
            unprocessed_bills += bills

        self.log.write('[{}]: collected {} bill IDs\n'.format(datetime.now(),
            len(unprocessed_bills)))

        valid_bill_fields = ['bill', 'about']
        bills = []

        try:
            # Parse each bill
            for i, bill in enumerate(unprocessed_bills):

                if i % round(len(unprocessed_bills)/4) == 0:
                    print('*** Processing {} of {} bills ***\n'.format(
                        i, len(unprocessed_bills)))

                s = ''
                bill_id = bill[0]
                self.log.write('[{}]: requesting bill from web page: {}\n'.format(
                        datetime.now(), self.web_page + bill[1]))
                page = requests.get(self.web_page + bill[1])
                soup = BeautifulSoup(page.text, 'html.parser')

                # Skip bill if we've already processed this text
                full_text = soup.get_text()
                loc = full_text.lower().find('date published')
                date = parser.parse(full_text[loc+16:loc+35])
                if bill_id in self.manifest and \
                        parser.parse(self.manifest[bill_id]) >= date:
                    self.log.write('[{}]: skipping bill {} -- no new info\n'.format(
                        datetime.now(), bill_id))
                    continue

                # Get preliminary information about the bill
                title = soup.find('div', {'id': 'bill_title'})
                intro_date = soup.find('td', {'id': 'bill_intro_date'})
                authors = soup.find('td', {'id': 'bill_authors'})
                fields = [title, intro_date, authors]
                for i, field in enumerate(fields):
                    fields[i] = field.get_text().strip().replace('\xa0', ' ') if field else 'N/A'
                title, intro_date, authors = fields

                # Concatenate bill sections and map them to bill ID...
                # Store HTML for display and cleaned string for classification
                bill_text = soup.find('div', {'id': 'bill_all'})
                for field in bill_text:
                    if 'id' in field.attrs \
                            and field.attrs['id'] in valid_bill_fields:
                       s += field.get_text()

                text = ' '.join(
                        s.replace('\xa0', ' ').replace('\n', ' ').replace('\t', ' ').split())

                bills.append({
                        'id': bill_id,
                        'title': title,
                        'date': intro_date,
                        'change_date': str(date),
                        'authors': authors,
                        'text': text,
                        'source': self.web_page + bill[1]})

                self.manifest[bill_id] = str(date)
        except Exception as e:
            self.log.write('[{}]: error occured while processing bills: {}\nwriting {} bills to JSON now\n'.format(
                    e, datetime.now(), len(bills)))
            if bills:
                json.dump(bills, open('data.json', 'w'))
            json.dump(self.manifest, open('manifest.json', 'w'))

        self.log.write('[{}]: collected info on {} bills\n'.format(
                datetime.now(), len(bills)))

        if bills:
            json.dump(bills, open('data.json', 'w'))
        json.dump(self.manifest, open('manifest.json', 'w'))


if __name__ == '__main__':
    web_page = 'https://leginfo.legislature.ca.gov'
    s = Scraper(web_page)
    s.fetch_docs()
