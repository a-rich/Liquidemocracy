Bill Collection
============================
This directory contains another directory called `scrapers` which has four
directories inside of it: `cities`, `counties`, `states`, and `federal`. Each
of these should contain a folder for every region at that governance level that
should have its legislation scraped. For example, `cities` contains a directory
called `san_francisco`, `counties` contains a directory called `san_francisco`
(San Francisco is both a city and a county; the legislation scraped in San
Francisco applies to both governance levels; the `san_francisco` directory in
`counties` is symbolically linked to the `san_francisco` directory in
`cities`), `states` contains a directory called `california`, and `federal`
contains no sub-directories since one scraper is used to collect all federal
legislation.

When expanding Liquidemocracy's bill collection functionality, please create an
appropriately named directory inside the directory corresponding to that
region's governance level. If there is a conflict in the directory names,
please append (e.g. the state initials) to the directory name so that it is
unique.

For example, if you want to add a scraper for the city of Berkeley, West
Virginia but there already exists a directory called `berkeley` (Berkeley,
California), then create a directory named `berkeley_wv`.

Scraper requirements
---------------------------
Each region's scraping directory *must* contain a file called `scraper.py`.
This module *must* create three files during its operation: `data.json`,
`exec.log`, and `manifest.json`.

*data.json*: This is a list of bills where each bill adheres to the format
specified below (see `Bill data requirements`).

*exec.log*: This file logs the activity of the scraper for debugging purposes.
All log entries shall begin with a square bracket enclosed datetime followed by
a colon followed by a description that indicates which task is about to be
performed. At the beginning of a scraper's execution, please print two blank
lines, a line of 75 hash symbols (`#`), a line stating something to the effect
of "[2018-03-15 16:14:18.350200]:  requesting from California state web page -
https://leginfo.legislature.ca.gov", and another line of 75 hash symbols. Each
successive log entry shall describe an, ideally, error prone operation that is
about to take place. For example, it may be a good idea to log HTTP requests,
data parsing, etc.

*manifest.json*: Scraping is a routine operation in Liquidemocracy. In order to
make the scraping functionality as lightweight as possible, developers of
scrapers *must* prevent redundant data collection. For example, the scraper for
the city of San Francisco locates PDF files on the city's web page and stores
the file names of these PDFs in a dictionary (`manifest.json`). Before
requesting the PDF data, the file name is cross-referenced in the manifest and
data collection is skipped if the file name is present in the manifest. The
website from which federal legislation is scraped lists all the bills and their
last modified date in a table. The table also includes a zip file which
contains all of these same bills. To minimize scraping time, one request is
made for the zip file instead of requsting each XML in the table. Since the
last modified data for each bill is included in the table, we can skip parsing
a bill in the zip archive if the manifest entry (a datetime) for that bill is
>= the date in the table. Unfortunately, the California state bill page
includes neither a zip archive nor a listing of last modified dates. As a
consequence, the scraper must make an independent request to every single
bill's web page making it the slowest scraper implemented thus far.

Bill data requirements
-----------------------------
`data.json` is the critically required output of a scraper's execution. It
*must* be a list containing a dictionary for each bill scraped. The following
specifies the required format for these bill dictionaries:

* *id*: The bill's unique ID

* *title*: A brief text description of the bill

* *date*: May be either the date the bill was introduced, or the last modified
  date

* *authors*: The representatives sponsoring the bill -- may be 'N/A' if no
  authors found

* *text*: The text body of the bill to be displayed to users

* *source*: The URL link to where this bill's data was collected from.

You may add more fields to the bill dictionary, but it is advised that
additions are minimized. For example, if two dates were located in the bill
(one for introuced date and the other for last modified date), you may place
one of them in the `date` field and create a new field called `change_date` or
`intro_date` for the other.


Install Slate
-------------------

#### Inside virtual enviornment: ###
`pip3.6 install https://github.com/timClicks/slate/archive/master.zip`

###  Fix relative path `utils` import: ###
Change line 25 of env/lib/python3.6/site-packages/slate/classes.py from:

`import utils`

to

`from slate import utils`
