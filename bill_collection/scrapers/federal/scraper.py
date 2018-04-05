import os
import io
import json
import zipfile
import requests
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
        self.log.write('[{}]:  requesting from federal government web page - {}'.format(
                datetime.now(), self.web_page))
        self.log.write('\n##############################################################################\n')

        print('*** Requesting from federal web page ***\n')

        def most_recent_bills():
            """
                Find the most recent congress (e.g. 115th) and then find the
                most recent session (e.g. 2nd).
            """

            # Find the most recent congress and then the most recent session
            url_tail = []
            for i in range(2):
                page = requests.get(self.web_page + '/'.join(url_tail))
                soup = BeautifulSoup(page.text, 'html.parser')
                anchors = [a for a in (td.find('a', href=True)
                        for td in soup.find_all('td')) if a
                        and 'bulkdata/BILLS/' in a['href']]
                links = []
                for i, a in enumerate(list(anchors)):
                    try:
                        links.append(int(a.get('href').split('/')[-1]))
                    except:
                        del anchors[i]
                url_tail.append(str(max(links)))

            # Fetch urls tails of bills and resolutions
            self.log.write('[{}]: requesting page with bill listings - {}\n'.format(
                    datetime.now(), self.web_page + '/'.join(url_tail)))
            page = requests.get(self.web_page + '/'.join(url_tail))
            soup = BeautifulSoup(page.text, 'html.parser')
            pages = [a.get('href').split('/')[-1]
                    for a in (td.find('a', href=True)
                    for td in soup.find_all('td')
                    if 'Parent Directory' not in td.get_text()) if a
                    and 'bulkdata/BILLS/' in a['href']]

            return ['/'.join(url_tail + [p]) for p in pages]

        def bill_date_pairs(p):
            """
                Returns a list of pairs containing the href for the bill and
                the date it was last modified. Also returns the ZipFile object.
            """

            self.log.write('[{}]: requesting bills to get (bill, date) pairs - {}\n'.format(
                    datetime.now(), self.web_page + p))
            page = requests.get(self.web_page + p)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Locate the zip archive on this page
            zip_url = next((a.get('href') for a in (td.find('a', href=True)
                    for td in soup.find_all('td') if td)
                    if a and '.zip' in a.get('href')))

            zip_r = requests.get(page.url + '/' + zip_url.split('/')[-1])
            zip_file = zipfile.ZipFile(io.BytesIO(zip_r.content))

            # Isolate unique bill numbers (sometimes there are multiple
            # slightly different files for the same bill)
            files = {}
            for obj in zip_file.filelist:
                string = obj.filename.split(page.url.split('/')[-1])[-1].split('.')[0]
                numbers = []
                for i, char in enumerate(string):
                    try:
                        numbers.append(str(int(char)))
                    except:
                        remainder = string[i+1:]
                        break
                if ''.join(numbers) not in files:
                    files[''.join(numbers)] = obj.filename

            # For each unique bill number, pair the href with the date
            pairs = []
            for href in files.values():
                tr = next((a.find_parent().find_parent()
                        for a in (td.find('a', href=True)
                        for td in soup.find_all('td'))
                        if a and a.get_text().strip() == href))
                chillen = []
                for i, td in enumerate(tr):
                    if td.name and not td.find('a'):
                        chillen.append(list(tr.children)[i])
                date = parser.parse(max([c.get_text() for c in chillen]))
                pairs.append((href, date))

            return pairs, zip_file

        def extract_info(zip_file, href, date):
            """

            """

            self.log.write('[{}]: processing zip object - {}\n'.format(
                    datetime.now(), href))
            zip_soup = BeautifulSoup(zip_file.open(href).read(), 'html.parser')

            try:
                bill_id = zip_soup.find('legis-num').get_text()
            except:
                bill_id = zip_soup.find('dc:title').get_text().split(':')[0]
            try:
                title = zip_soup.find('official-title').get_text()
            except:
                title = ' '.join(zip_soup.find('dc:title').get_text().split(':')[1:])
            try:
                text = zip_soup.find('legis-body').get_text()
            except:
                try:
                    text = zip_soup.find('resolution-body').get_text()
                except:
                    text = zip_soup.find('engrossed-amendment-body').get_text()
            try:
                authors = zip_soup.find('sponsor').get_text()
            except:
                authors = 'N/A'

            self.manifest[href] = str(date)

            return {
                'id': bill_id,
                'title': title,
                'date': str(date),
                'authors': authors,
                'text': text,
                'source': self.web_page + page + '/' + href}


        bills = []
        pages = most_recent_bills()
        for i, page in enumerate(pages):

            if i % round(len(pages)/4) == 0:
                print('*** Processing page {} of {} ***\n'.format(
                    i, len(pages)))

            pairs, zip_file = bill_date_pairs(page)

            for j, (href, date) in enumerate(pairs):

                if j % round(len(pairs)/4) == 0:
                    print('\t*** Processing bill {} of {} ***\n'.format(
                        j, len(pairs)))

                if href in self.manifest:
                    if date > parser.parse(self.manifest[href]):
                        bills.append(extract_info(zip_file, href, date))
                    self.log.write('[{}]: no new changes to {}\n'.format(datetime.now(), href))
                else:
                    bills.append(extract_info(zip_file, href, date))

        json.dump(self.manifest, open('manifest.json', 'w'))
        json.dump(bills, open('data.json', 'w'))

if __name__ == '__main__':
    web_page = 'https://www.gpo.gov/fdsys/bulkdata/BILLS/'
    s = Scraper(web_page)
    s.fetch_docs()
