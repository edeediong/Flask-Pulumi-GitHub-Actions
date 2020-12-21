"""A basic test written with unittest to test flask application."""

import unittest
import json

from app import app

class CitiesTestCase(unittest.TestCase):

    def test_cities(self):
        tester = app.test_client(self)
        response = tester.get('/cities.json', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), json.dumps(['Amsterdam', 'San Francisco', 'Berlin', 'New York']))

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.data.decode("utf-8"), "Hello, World! (from a Docker container)")

if __name__ == '__main__':
    unittest.main()
