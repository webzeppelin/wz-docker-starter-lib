import unittest
import json

from flask_app import services, config
#from ..flask_app.config import app, configure_app
class ServiceTestCase(unittest.TestCase):

    def setUp(self):
        # return
        config.configure_app(config.app)
        self.test_client = config.app.test_client()

    def test_time(self):
        #server_time = services.get_time()
        response = self.test_client.get('/api/v1/time')
        self.assert_success_and_json(response)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertIsNotNone(json_data)
        print(json.dumps(json_data))

    def test_sign_guestbook(self):
        response = self.test_client.post('/api/v1/guestbook', data = json.dumps({ "name": "Andy", "message": "Hello world!"}), content_type='application/json')
        self.assert_success_and_json(response)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_data)
        print(json.dumps(json_data))

    def test_browse_guestbook(self):
        response = self.test_client.get('/api/v1/guestbook')
        self.assert_success_and_json(response)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_data)
        print(json.dumps(json_data))

    def test_browse_guestbook_more(self):
        response = self.test_client.get('/api/v1/guestbook?last_id=6fa459ea-ee8a-3ca4-894e-db77e160355e')
        self.assert_success_and_json(response)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_data)
        print(json.dumps(json_data))

    def assert_success_and_json(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')