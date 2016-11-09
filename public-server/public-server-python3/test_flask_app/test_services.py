import unittest
import json

from flask_app import services, config
from flask_app.utils import oidc
from .test_oidc import OIDCTestCase

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
        response = self.test_client.get('/api/v1/guestbook?last_id=10')
        self.assert_success_and_json(response)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_data)
        print(json.dumps(json_data))

    def test_login_start(self):
        response = self.test_client.get('/api/v1/login')
        self.assert_success_and_json(response)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_data)
        print(json.dumps(json_data))

    def test_login_start_with_parms(self):
        response = self.test_client.get('/api/v1/login?scope=openid+email+profile')
        self.assert_success_and_json(response)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_data)
        print(json.dumps(json_data))

    def test_login_complete(self):
        client = oidc.OIDCClient(config.app.oidc_config)
        tokens = OIDCTestCase.simulate_login(client)
        self.assertIsNotNone(tokens)

        headers = {
            'Authorization': 'Bearer '+tokens.access_token
        }
        response = self.test_client.get('/api/v1/login/info', headers=headers)
        self.assert_success_and_json(response)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_data)
        print(json.dumps(json_data))

    def assert_success_and_json(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')

