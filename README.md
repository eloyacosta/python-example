# Intro

  This is an example of an small python API, using [Flask](http://flask.pocoo.org) framework.

# Installation

1. **Install [Python](https://www.python.org/downloads/)**
2. **Install [Flask](http://flask.pocoo.org/docs/0.10/installation/#installation)**
3. **Clone this repo to your prefered route in the local fs (ej: ~/git/)** 
  - Create dir

     ``$ mkdir ~/git``

  - Change to dir 

     ``$ cd ~/git``

  - Git clone 

     ``$ git clone https://github.com/eloyacosta/python-example.git``

4. **Exec command:**

     ``$ python python-example/app.py``
     
     This will make python to keep running and listening on port 5000.

# Some request testing

  **Note:** You can use other shell to test the progran using CURL.

1. **You can try to post some data**

     ``curl -X POST http://127.0.0.1:5000/ep1 -H "Accept: application/json" -H "Content-Type: application/json" -d '[{"date": "2015-11-20T14:48:00.451765", "uid": "3", "name": "Perry Manson", "md5checksum": "2ebf36e266bae03f4f7c312d9c82a052"},{"date": "2015-11-20T14:50:00.451766", "uid": "4", "name": "Eloy Acosta", "md5checksum": "c193dab16230b3ef1eafc64570cff69e"},{"date": "2015-11-19T10:20:00.451770", "uid": "1", "name": "DataRobot user", "md5checksum": "8949b7957f976a5f0f4e8e88316f3cc6"},{"date": "2015-11-20T14:53:00.451768", "uid": "4", "name": "Eloy Acosta", "md5checksum": "6067ce211d11fc938e5ad835d82412b1"},{"date": "2015-11-20T12:00:00.451769", "uid": "3", "name": "Perry Manson", "md5checksum": "987ae0f34facc13a5b38434b5293a9e5"},{"date": "2015-11-19T10:20:00.451770", "uid": "1", "name": "DataRobot user", "md5checksum": "8949b7957f976a5f0f4e8e88316f3cc6"}]'``

2. **You can query the API**

     ``$ curl -i -X GET http://127.0.0.1:5000/ep2?uid=1&date=2015-11-19"``

# Unit Tests 

  All the app tests has been written with [Unittest](https://docs.python.org/2/library/unittest.html).
  To run the tests, be sure you are in the project directory (i.e: ~/git/python/example) and exec:

  ``$ python test.py``
