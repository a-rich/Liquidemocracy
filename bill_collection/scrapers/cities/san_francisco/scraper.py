import os
import re
import sys
import json
import slate
import requests
from time import time
from dateutil import parser
from datetime import datetime
from bs4 import BeautifulSoup


class Scraper():
    web_page = None
    log = None
    manifest = None
    file_source_map = {}

    def __init__(self, web_page):
        """
            Open log files to track requests, PDF writting, and PDF parsing.
            Fetch PDFs from web page and parse them to from bills.
        """

        self.web_page = web_page
        self.log = open('exec.log', 'a')

        if os.path.exists('manifest.json'):
            self.manifest = json.load(open('manifest.json', 'r'))
        else:
            self.manifest = {}

    def fetch_docs(self):
        """
            Fetch PDF docs from SF web page and write them to disk.
        """

        # Helper to log when finding a PDF that's been downloaded already.
        def log_repeat(link):
            self.log.write('[{}]:  file {} has already been scraped\n'.format(
                    datetime.now(), link.split('/')[-1]))
            print("\tFile {} already downloaded.".format(link.split('/')[-1]))

        # Helper to request PDF object and record the source link.
        def get_pdf(link):
            url = 'http://sfbos.org/' + link
            try:
                self.file_source_map[link.split('/')[-1]] = url
                return requests.get(url)
            except:
                self.log.write('[{}]:  could not request PDF {}\n'.format(
                        datetime.now(), url))

        # Log the beginning of the task
        self.log.write('\n\n##############################################################################\n')
        self.log.write('[{}]:  requesting from SF city web page - {}'.format(
                datetime.now(), self.web_page))
        self.log.write('\n##############################################################################\n')

        # Get the HTML from the web page and locate the listing of documents.
        divider = []
        try:
            print("Requesting data from San Francisco's 'introduced " \
                    "legislation' web page...")
            legislation = requests.get(self.web_page)
            soup = BeautifulSoup(legislation.text, 'html.parser')
            divider = soup.find_all('td', {'class': 'v_divider'})
            print("Retrieved data from the page.")
        except Exception as e:
            self.log.write('[{}]:  could not fetch bill page - {}\n'.format(
                    datetime.now(), e))

        # There should only be one list of proposed legislation.
        if len(divider) != 1:
            self.log.write('[{}]:  did not find one element when searching for the bill container - {}\n'.format(datetime.now(), divider))
            sys.exit()

        # Find all the links to PDFs and fetch the content.
        doc_links = [d['href'] for d in divider[0].find_all('a', href=True)]
        if not doc_links:
            self.log.write('[{}]:  could not find links to the PDF(s)\n'.format(
                    datetime.now()))
        print("\tRequesting PDFs from links found on the web page...")
        docs = [get_pdf(link) if link.split('/')[-1] not in self.manifest
                else log_repeat(link) for link in doc_links]

        # For all the fetched documents, write them to disk as a PDF.
        for doc, link in zip(docs, doc_links):

            if link.split('/')[-1] in self.manifest:
                continue

            doc.encoding = 'utf-8'
            os.makedirs('docs' , exist_ok=True)
            with open('docs/'+link.split('/')[-1], 'wb') as f:
                try:
                    print('\tWriting {} to disk...'.format(link.split('/')[-1]), end=' ')
                    f.write(doc.content)
                    self.log.write('[{}]:  wrote {} to file\n'.format(
                            datetime.now(), link.split('/')[-1]))
                    print('wrote {}.'.format(link.split('/')[-1]))
                except Exception as e:
                    self.log.write('[{}]:  {}\nduring write of {}\n'.format(
                            datetime.now(), e, link.split('/')[-1]))

        self.parse_docs()
        self.log.close()

    def parse_docs(self):
        """
            Parse PDF docs to create Bills.
        """

        # Helper to parse PDF in order to represent and classify its contents.
        def process_doc(doc):
            text = '\n'.join(doc).lower()

            IDs = [r.strip() for r in re.findall(r'\n\d{6,6}\n', text)]
            titles = [r.strip() for r in re.findall(r'\n\[([^]]*)\]\n', text)]
            items = [r.strip() for r in re.split(r'\n\[[^]]*\]\n', text)]
            heading = items.pop(0)  # parse this for date and "introduced by"
            dt = parser.parse(re.findall(r'\n[a-z]+, [a-z]+ \d{1,2}, \d{4,4}\n', heading)[0].strip())
            sponsors, bodies = [], []

            for i in items:
                # Get the sponsor(s), if any
                s = re.findall(r'sponsor[s]*:[^\n]+', i)
                if s:
                    sponsors.append([r.strip() for r in re.split(r'; |, |and',
                            s[0].split(': ')[-1])])
                else:
                    sponsors.append([])

                # Everything after the sponsors line, if any.
                rest = re.split(r'[\n]*sponsor[s]*:[^\n]+', i)[-1]

                # Split on end of page (page number).
                text = re.split(r'- [0-9]+ -', rest)[0].strip('\n').replace('\n', '')

                bodies.append(text)

            # Ensure that all the collected bill attributes were scraped in
            # equal proportions.
            if not all(len(l) == len(IDs) for l in [titles, sponsors, bodies]):
                self.log.write('[{}]:  did not scrape the same number elements for each bill attribute\n'.format(datetime.now()))

            # Create Bill object and append it to bills list.
            for ID, title, sponsor, body in zip(IDs, titles, sponsors, bodies):
                bills.append({
                        'id': ID,
                        'title': title,
                        'date': str(dt),
                        'authors': sponsor,
                        'text': body,
                        'source': self.file_source_map[pdf]})

            if pdf not in self.manifest:
                self.manifest[pdf] = True

        # If bills file exists, load it; else create an empty list.
        print('\nParsing PDF data...')
        bills = []

        if not os.listdir('docs'):
            print('No new PDF documents to parse.')
            self.log.write('[{}]:  no new PDF documents to parse\n'.format(
                    datetime.now()))
            return

        # Iterate over PDFs in `docs` directory and parse them into objects.
        print('\tExtracting text from PDFs.')
        for pdf in os.listdir('docs'):

            with open('docs/'+ pdf, 'rb') as f:
                try:
                    doc = slate.PDF(f)
                except Exception as e:
                    self.log.write('[{}]:  {}\nduring slate.PDF() call on {}\n'.format(
                            datetime.now(), e, pdf))

            process_doc(doc)

        print('\tFinished extracting text.')

        # If data was dumped, delete all PDFs from the `docs` directory.
        try:
            json.dump(bills, open('data.json', 'w'))
            json.dump(self.manifest, open('manifest.json', 'w'))
            list(map(os.unlink, (os.path.join('docs',f) for f in
                    os.listdir('docs'))))
        except Exception as e:
            self.log.write('[{}]:  could not write JSON file - {}\n'.format(datetime.now(), e))


if __name__ == '__main__':
    web_page = 'http://sfbos.org/legislation-introduced'
    s = Scraper(web_page)
    s.fetch_docs()
