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

    def __init__(self, web_page):
        self.web_page = web_page

    def fetch_docs(self):

        def write_data(bills, subject='other'):
            if os.path.exists('other.json'):
                data = json.load(open('other.json', 'r'))
            else:
                data = {}

            if subject in data:
                data[subject] += bills
            else:
                data[subject] = bills

            json.dump(data, open('other.json', 'w'))

        def collect_bills(bill_divs):
            root = 'https://www.congress.gov'
            bill_texts = []
            links = [b.find('a')['href'] for b in bill_divs]
            for l in links:
                print('\t\tVisiting:', l)
                page = requests.get(l, headers={'User-agent': 'bill collection'})
                soup = BeautifulSoup(page.text, 'html.parser')

                try:
                    text = [a for a in soup.find('ul',
                                    {'class': 'tabs_links'}).find_all('a')
                            if 'text' in a['href']][0]
                except:
                    print('\n{}\n'.format('FAILURE: could not find tabs_links'))
                    continue

                # Check if there is any text info
                is_text = text.find('span', {'class': 'counter'}).get_text()

                print('is_text: {}'.format(is_text))

                if is_text:
                    text_link = text['href']
                    page = requests.get(root + text_link,
                            headers={'User-agent': 'bill collection'})
                    soup = BeautifulSoup(page.text, 'html.parser')
                    text_container = soup.find('div', {'class': 'generated-html-container'})

                    if not text_container:
                        text_container = soup.find('pre',
                                {'id': 'billTextContainer'})

                    if not text_container:
                        print("ERROR -- text_container is None")
                        continue

                    text = ' '.join(text_container.get_text().split())
                    bill_texts.append(text)

            print(len(bill_texts))

            return bill_texts

        subjects = [
                'Taxation',
                'Health',
                'Armed Forces and National Security',
                'Foreign Trade and International Finance',
                'International Affairs',
                'Crime and Law Enforcement',
                'Transportation and Public Works',
                'Education',
                'Energy',
                'Agriculture and Food',
                'Economics and Public Finance',
                'Labor and Employment',
                'Environmental Protection',
                'Science, Technology, Communications',
                'Immigration'
                ]

        others = [
                'Government Operations and Politics',
                'Congress',
                'Public Lands and Natural Resources',
                'Social Welfare',
                'Finance and Financial Sector',
                'Commerce',
                'Law',
                'Housing and Community Development',
                'Water Resources Development',
                'Native Americans',
                'Civil Rights and Liberties, Minority Issues',
                'Emergency Management',
                'Families',
                'Animals',
                'Arts, Culture, Religion',
                'Sports and Recreation',
                'Social Sciences and History'
                ]

        # Request the bill listing for each subject
        for subject in subjects:
            link = self.web_page.format('+'.join(subject.split(' ')))
            page = requests.get(link, headers={'User-agent': 'bill collection'})
            soup = BeautifulSoup(page.text, 'html.parser')
            bill_count = soup.find('span', {'class': 'results-number'})
            bill_divs = soup.find_all('li', {'class': 'expanded'})
            page_number = 2

            try:
                bill_count = int(bill_count.get_text().split('of')[-1].strip().replace(',', ''))
            except:
                print('ERROR: could not get the total number of bills for this subject')

            try:
                last_bill_on_page = [int(str(b).strip().replace(',', '').replace('.', ''))
                                    for i, b in enumerate(bill_divs[-1]) if i == 2][0]
            except:
                print("ERROR: could not get last bill's number")

            print('Collecting {} bills on the subject of {}'.format(bill_count, subject))

            # Collect the first page of bills and write to JSON file
            write_data(collect_bills(bill_divs), subject)

            limit = 3000
            #limit = 175

            # Iterate through all the pages for this subject
            while last_bill_on_page < min(limit, bill_count):
                print('\tProcessed {} bills so far -- requesting page {}'.format(last_bill_on_page, page_number))
                next_link = link + "&page={}".format(page_number)
                page = requests.get(next_link, headers={'User-agent': 'bill collection'})
                soup = BeautifulSoup(page.text, 'html.parser')
                bill_divs = soup.find_all('li', {'class': 'expanded'})

                try:
                    last_bill_on_page = [int(str(b).strip().replace(',', '').replace('.', ''))
                                        for i, b in enumerate(bill_divs[-1]) if i == 2][0]
                except:
                    print("ERROR: could not get last bill's number")

                if last_bill_on_page > limit:
                    bill_divs = bill_divs[:(limit % len(bill_divs))]

                write_data(collect_bills(bill_divs), subject)
                page_number += 1


if __name__ == '__main__':
    web_page = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22subject%22%3A%22{}%22%7D"
    s = Scraper(web_page)
    s.fetch_docs()
