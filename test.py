#Application test by eloy.acosta@gmail.com

import unittest
import json
from pymongo import MongoClient
from app import app #myapp 


class MyTestClass(unittest.TestCase):
    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass

    # clean up logic for the test suite declared in the test module
    # code that is executed after all tests in one test run
    # This could be useful to delete the tests inserted data 
    @classmethod
    def tearDownClass(cls):
        pass

    # initialization logic
    # code that is executed before each test
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        self.app.debug = True
        pass

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    def test_get_no_parameters(self):
        #  sends HTTP GET request to the application
        #  on the specified path
        result = self.app.get('/ep2')
        # assert the status code of the response
        data_expected = dict(success = 'false', message='A valid UID must be provided')
        data_recieved = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data_expected, data_recieved)

    def test_get_ok(self):
        #  sends HTTP GET request to the application
        #  on the specified path
        result = self.app.get('/ep2?uid=1&date=2012-01-01')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


    def test_get_no_uid(self):
        #  sends HTTP GET request to the application
        #  on the specified path
        result = self.app.get('/ep2?date=2015-03-12')
        # assert the status code of the response
        data_expected = dict(success = 'false', message='A valid UID must be provided')
        data_recieved = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data_expected, data_recieved)


    def test_post_everything_ok(self):
        data_to_send = [{'date': '2015-11-20T14:48:00.451765', 'uid': '3', 'name': 'Perry Manson',
                         'md5checksum': '2ebf36e266bae03f4f7c312d9c82a052'},
                        {'date': '2015-11-20T14:50:00.451766', 'uid': '4', 'name': 'Eloy Acosta',
                         'md5checksum': 'c193dab16230b3ef1eafc64570cff69e'},
                        {'date': '2015-11-20T14:51:00.451767', 'uid': '4', 'name': 'Eloy Acosta',
                         'md5checksum': '424d1733757be8d10d22077bd9fb24ad'},
                        {'date': '2015-11-20T14:53:00.451768', 'uid': '4', 'name': 'Eloy Acosta',
                         'md5checksum': '6067ce211d11fc938e5ad835d82412b1'},
                        {'date': '2015-11-20T12:00:00.451769', 'uid': '3', 'name': 'Perry Manson',
                         'md5checksum': '987ae0f34facc13a5b38434b5293a9e5'},
                        {'date': '2015-11-19T10:20:00.451770', 'uid': '1', 'name': 'DataRobot user',
                         'md5checksum': '8949b7957f976a5f0f4e8e88316f3cc6'}]

        data_to_send = json.dumps(data_to_send)
        headers = [('Content-Type', 'application/json')]
        result = self.app.post('/ep1', headers=headers, data=data_to_send)

        data_expected = dict(message='INFO: 6 element/s successfully saved', success='true')
        data_recieved = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data_expected, data_recieved)

    def test_post_some_wrong(self):
        data_to_send = [{'date': '2015-11-20T14:48:00.451765', 'uid': '3', 'name': 'Perry Manson',
                         'md5checksum': '2ebf36e266bae03f4f7c312d9c82a052'},
                        {'date': '2015-11-20T14:50:00.451766', 'uid': '4', 'name': 'Eloy Acosta',
                         'md5checksum': 'c193dab16230b3ef1eafc64570cff69e'},
                        {'date': '2015-11-20T14:51:00.451767', 'uid': '4', 'name': 'Eloy Acosta',
                         'md5checksum': '424d1733757be8d10d22077bd9fb24ad'},
                        {'date': '2015-11-20T14:53:00.451768', 'uid': '4', 'name': 'Eloy Acostakkkkk',
                         'md5checksum': '6067ce211d11fc938e5ad835d82412b1'},
                        {'date': '2015-11-20T12:00:00.451769', 'uid': '3', 'name': 'Perry Manson',
                         'md5checksum': '987ae0f34facc13a5b38434b5293a9e5'},
                        {'date': '2015-11-19T10:20:00.451770', 'uid': '1', 'name': 'DataRobot user',
                         'md5checksum': '8949b7957f976a5f0f4e8e88316f3cc6'}]

        data_to_send = json.dumps(data_to_send)
        headers = [('Content-Type', 'application/json')]
        result = self.app.post('/ep1', headers=headers, data=data_to_send)

        data_expected = dict(message='Invalid checksum or field type for some elements', success='false')
        data_recieved = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data_expected, data_recieved)

    def test_post_method_not_allowed(self):
        data_to_send = 'I am sending something using GET method to test'

        data_to_send = json.dumps(data_to_send)
        result = self.app.get('/ep1', data=data_to_send)

        self.assertEqual(result.status_code, 405)

# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
