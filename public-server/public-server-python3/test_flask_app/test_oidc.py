import unittest
import json

import flask_app
import requests
import urllib
from flask_app import config
from flask_app.utils import oidc

class OIDCTestCase(unittest.TestCase):

    def setUp(self):
        config.configure_app(config.app)
        self.oidc_config = config.app.oidc_config

    def test_get_metadata(self):
        metadata_url = self.oidc_config.metadata_url
        print('metadata_url: '+metadata_url)
        metadata_cache = oidc.OIDCMetadataCache()
        metadata = metadata_cache.get_metadata(metadata_url)
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.issuer, 'https://idp.wzstarter.org/dex')
        print(json.dumps(metadata.__dict__))

    def test_get_login_url(self):
        client = oidc.OIDCClient(self.oidc_config)
        login_url = client.get_login_url('https://app.wzstarter.org/')
        self.assertIsNotNone(login_url)
        print(login_url)

    def test_simulate_login(self):
        client = oidc.OIDCClient(self.oidc_config)
        tokens = OIDCTestCase.simulate_login(client)
        print("tokens -> " + json.dumps(tokens.__dict__))
        self.assertIsNotNone(tokens)

    @classmethod
    def simulate_login(cls, client):
        login_url = client.get_login_url('https://app.wzstarter.org/', scope="openid email profile")+"&connector_id=local"
        print("login_url: "+login_url)
        resp = requests.get(url=login_url, verify=False, allow_redirects=False)

        login_session_url = resp.headers.get('Location')
        print("login_session_url: "+login_session_url)
        qs = urllib.parse.urlparse(login_session_url).query
        qs_dict = urllib.parse.parse_qs(qs)
        session_key = qs_dict['session_key'][0]
        prompt = qs_dict.get("prompt", [""])[0]

        login_form_action_url = 'https://idp.wzstarter.org/dex/auth/local/login?prompt='+urllib.parse.quote(prompt)+'&session_key='+urllib.parse.quote(session_key)
        print("login_form_action_url: "+login_form_action_url)
        login_form_payload = {
            'userid': 'user1@wzstarter.org',
            'password': 'password'
        }
        login_resp = requests.post(url=login_form_action_url, data=login_form_payload, verify=False, allow_redirects=False)

        login_redirect_url = login_resp.headers.get('Location')
        print("login_redirect_url: "+login_redirect_url)
        code_qs = urllib.parse.urlparse(login_redirect_url).query
        code_qs_dict = urllib.parse.parse_qs(code_qs)
        code = code_qs_dict['code'][0]
        state = code_qs_dict['state'][0]

        return client.get_tokens('https://app.wzstarter.org/', code)



