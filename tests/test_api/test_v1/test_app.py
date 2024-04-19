#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
import unittest
from flask import json
from api.v1 import app

class TestApp(unittest.TestCase):
    """Tests to check the effectiveness of app"""

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_404_error_handler(self):
        response = self.app.get('/nonexistent_endpoint')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Not found')
