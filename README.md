Liquidemocracy is comprised of two distinct components; the React application which is the client code, and the Flask server which the React app interacts with through a JSON RESTful API to access back end resources.

Viewing an already deployed project
----------------------------------------------------

To view and interact with an already deployed and operational instance, please go to http://liquidemocracy.herokuapp.com and create an account with Liquidemocracy. This site houses our Heroku deployment of the React application which makes requests to http://liquidemocracy-api.herokuapp.com which is a separate Heroku deployment of the Flask server.

Building the project from scratch
----------------------------------------------------

As mentioned above, Liquidemocracy is two separate applications that interact through a JSON RESTful API. The purpose for this is facilitate the development of multiple front ends, web or mobile applications, which interact with the same back end; it also encourages development of backend resources that need only to share a common URL interface with the independent front ends.

### Building the Flask (server) application

#### Install MongoDB for your operating system:

https://docs.mongodb.com/manual/installation/

#### Install Python 3.5.2 for your operating system:

https://www.python.org/downloads/

* **Clone the repository that holds the back end code:**

`git clone https://github.com/a-rich/Liquidemocracy.git`

* **Create a Python3.5 virtual environment and activate it**

`python3.5 -m venv env && source env/bin/activate`

**NOTE:** depending on your operating system and your Python 3.5 installation, you might receive an error message similar to this one:

`Error: Command '['liquidemocracy-api/env/bin/python3.5', '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1`

If this occurs, you must create the virtual environment without pip and activate it:

`python3.5 -m venv env --without-pip && source env/bin/activate`

and then install pip using the `get-pip.py` script which is located in the root of the repository:

`python3.5 get-pip.py`

If, for some reason, the `get-pip.py` script is not in the repository, you can download it:

`wget https://bootstrap.pypa.io/get-pip.py`

* **Install the required packages using the `setup.py` script (this may take awhile if you do not have cached versions of NumPy and SciPy):**

`pip3 install -e .`

* **Set environment variables:**

`export FLASK_APP=liquidemocracy`

`export FLASK_DEBUG=true`

* **Run the app:**

`flask run`

### A note about testing the API

This API does not serve any HTML so, unless you know the URL route for the GET endpoints and the required info to use them, you will not be able to successfully interact with the API through the browser. You may, however, use Postman to simulate requests to the many endpoints and confirm that the API works as expected, but doing so would require careful inspection of the different API files in `liquidemocracy/views/`. An easier way to interact with the local Flask server instance would be to start up a local React application instance, do a search for all the `http://liquidemocracy-api.herokuapp.com` strings used in the `axios.get` and `axios.post` function calls and replace them with `http://localhost:5000`. **By far the easiest way to test the application would be to use the already deployed instances of the React and Flask applications (see the instructions at the very top)**.

### Building the React (client) application

#### Install Node.js:

https://www.npmjs.com/get-npm

### Fetch all remotes of the main repository (the same one from the "building the Flask (server) application" instructions):

`git fetch --all`

### Checkout the `views` branch:

`git checkout origin/views`

### Install NPM packages

`npm install`

### Build and start the React app

`npm run build && npm start`

### Visit the React application by going to `localhost:8080` in your browser

If everything was ran correctly, you should be able to go to localhost:8080 and the website should be visible. Make sure you have nothing else running on port 8080. If so, you can modify the server.js file and manually change the port number in app.listen().

Testing the individual back end services
--------------------------------------------------------

The above instructions suffice to test the main applications. If you wish to test the bill scraper, classifier, and recommender also, this will require a few more steps. Remember, every file here must be executed inside the virtual environment constructed in the steps above.

* **Install the proper version of `slate` for extracting text information from PDFs:**

`pip3 install git+https://github.com/timClicks/slate`

* **Modify a slate package file to fix import error:**

`vim env/lib//python3.5/site-packages/slate/classes.py`
Change line 25 from `import utils` to `from . import utils`

* **Run scraping routine:**

`cd liquidemocracy/bill_collection && python3.5 routine.py`

This will run all the scrapers one after another, classify the resulting set of bill texts, and then insert them into the MongoDB collection for Bill documents. If you wish to test the individual scrapers, then navigate the various subdirectories of `/liquidemocracy/bill_collection/scrapers` and run:

`python3.5 scraper.py`

### Testing the bill classifier

Testing the bill classification module, by itself, requires having collected bills and having them formatted in the way that `routine.py` does -- that script will, as part of its operation, also test the classifier. If you wish to manually run the classifier, then we recommend commenting out the `os.unlink` line that removes the `data.json` file after classification so you can run the `classify_bills.py` script by hand.

### Testing the bill recommender

Testing the bill recommender module is a little more difficult since the functions require user objects passed in at runtime. The easiest way to test the recommender module would be to use the React front end to click on and voting on a bunch of bills controlling for the policy area (change the selection of the category dropdown) so that your user interest vector received positive signals for those policy areas. Then choose “recommended” from the filter dropdown to hit the endpoint which runs the bill recommender script to fetch and display recommended bills only.

