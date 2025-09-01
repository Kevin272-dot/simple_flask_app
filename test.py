from flask import Flask
from flask_testing import TestCase
import unittest
app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, World!"


class MyTestCase(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_index(self):
        response = self.client.get('/')
        self.assert_200(response)
        self.assertEqual(response.data.decode(), "Hello, World!")


if __name__ == '__main__':
    unittest.main()
