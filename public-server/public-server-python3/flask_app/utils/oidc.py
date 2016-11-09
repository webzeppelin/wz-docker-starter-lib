import threading
#import base64
#import os
#from math import floor
from ..config import OIDCConfig
from ..config import app
import requests
import random
#from requests.utils import urlparse
from urllib.parse import urlencode
import jwt.algorithms
import jwt
import json
import base64
from .jwthack import from_jwk

class OIDCClient(object):
    def __init__(self, oidc_config):
        self.oidc_config = oidc_config
        self.idp_metadata = OIDCMetadataCache().get_metadata(oidc_config.metadata_url)

    def get_login_url(self, redirect_uri, scope='openid', state=None):
        if not state:
            state = OIDCClient.gen_nonce()
        params = {
            'response_type': 'code',
            'scope': scope,
            'client_id': self.oidc_config.client_id,
            'state': state,
            'redirect_uri': redirect_uri
        }
        return self.idp_metadata.authorization_endpoint + '?' + urlencode(params)

    def get_tokens(self, redirect_uri, code):
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }
        print("Token endpoint: "+self.idp_metadata.token_endpoint)
        resp = requests.post(self.idp_metadata.token_endpoint, data=payload, auth=(self.oidc_config.client_id, self.oidc_config.client_secret), allow_redirects=False, verify=False)

        if (resp.status_code != 200):
            raise OIDCError('Unexpected response code from token service','OIDCClient.get_id_token')

        jsobj = resp.json()
        tokens = OIDCTokens(vals=jsobj)
        self.validate_tokens(tokens)
        return tokens

    def validate_tokens(self, tokens):
        # validate the identity token first
        self.validate_token(tokens.id_token)
        self.validate_token(tokens.access_token)

    def validate_token(self, jwtoken):
        # for non-prod - workaround for bug in current version of PyJWT
        options = {
            'verify_exp': False
        }
        header_segment = jwtoken.split('.')[0]
        header = json.loads(OIDCClient.base64url_decode(header_segment).decode('utf-8'))
        kid = header['kid']
        key = OIDCKeystoreCache().get_key(self.idp_metadata.jwks_uri, kid)
        try:
            dectok = jwt.decode(jwtoken, key=key, audience='APP-WZSTARTER-ORG', options=options)
            print(str(dectok))
            return dectok
        except:
            raise OIDCError("Invalid JWT received", "OIDCClient.validate_jwt")


    @staticmethod
    def base64url_decode(input):
        if isinstance(input, str):
            input = input.encode('ascii')

        rem = len(input) % 4

        if rem > 0:
            input += b'=' * (4 - rem)

        return base64.urlsafe_b64decode(input)

    @staticmethod
    def gen_nonce():
        length = 10
        """ Generates a random string of bytes, base64 encoded """
        #if length < 1:
        #    return ''
        #string = base64.b64encode(os.urandom(length), altchars=b'-_')
        #b64len = 4 * floor(length, 3)
        #if length % 3 == 1:
        #    b64len += 2
        #elif length % 3 == 2:
        #    b64len += 3
        #return string[0:b64len].decode()
        return ''.join([str(random.SystemRandom().randint(0, 9)) for i in range(length)])

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class OIDCError(Error):
    def __init__(self, error, context):
        self.error = error
        self.context = context


# Based on tornado.ioloop.IOLoop.instance() approach.
# See https://github.com/facebook/tornado
class SingletonMixin(object):
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance


class OIDCMetadata(object):

    def __init__(self, issuer=None, authorization_endpoint=None, token_endpoint=None, jwks_uri=None, response_types_supported=[], grant_types_supported=[], subject_types_supported=[], id_token_signing_alg_values_supported=[], token_endpoint_auth_methods_supported=[], vals=None):
        self.issuer = issuer
        self.authorization_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint
        self.jwks_uri = jwks_uri
        self.response_types_supported = response_types_supported
        self.grant_types_supported = grant_types_supported
        self.subject_types_supported = subject_types_supported
        self.id_token_signing_alg_values_supported = id_token_signing_alg_values_supported
        self.token_endpoint_auth_methods_supported = token_endpoint_auth_methods_supported

        if vals:
            self.issuer = vals.get("issuer", self.issuer)
            self.authorization_endpoint = vals.get("authorization_endpoint", self.authorization_endpoint)
            self.token_endpoint = vals.get("token_endpoint", self.token_endpoint)
            self.jwks_uri = vals.get("jwks_uri", self.jwks_uri)
            self.response_types_supported = vals.get("response_types_supported", self.response_types_supported)
            self.grant_types_supported = vals.get("grant_types_supported", self.grant_types_supported)
            self.subject_types_supported = vals.get("subject_types_supported", self.subject_types_supported)
            self.id_token_signing_alg_values_supported = vals.get("id_token_signing_alg_values_supported", self.id_token_signing_alg_values_supported)
            self.token_endpoint_auth_methods_supported = vals.get("token_endpoint_auth_methods_supported", self.token_endpoint_auth_methods_supported)

class OIDCTokens(object):
    def __init__(self, id_token=None, token_type=None, access_token=None, expires_in=None, vals=None):
        self.id_token = id_token
        self.token_type = token_type
        self.access_token = access_token
        self.expires_in = expires_in

        if vals:
            self.id_token = vals.get('id_token', self.id_token)
            self.token_type = vals.get('token_type', self.token_type)
            self.access_token = vals.get('access_token', self.access_token)
            self.expires_in = vals.get('expires_in', self.expires_in)

    def to_dict(self):
        return self.__dict__

class OIDCMetadataCache(SingletonMixin):

    def __init__(self):
        self.metadata = {}
        self.metadata_lock = threading.Lock()

    def get_metadata(self, metadata_url):
        meta_tuple = self.metadata.get(metadata_url, None)
        if not meta_tuple:
            with self.metadata_lock:
                meta_tuple = self.metadata.get(metadata_url, None)
                if not meta_tuple:
                    meta_tuple = (threading.Lock(), None)
                    self.metadata[metadata_url] = meta_tuple
        if not meta_tuple[1]:
            with meta_tuple[0]:
                meta_tuple = self.metadata[metadata_url]
                if not meta_tuple[1]:
                    meta_tuple = (meta_tuple[0], self.load_metadata(metadata_url))
                    self.metadata[metadata_url] = meta_tuple
        return meta_tuple[1]

    def load_metadata(self, metadata_url):
        resp = None
        try:
            resp = requests.get(url=metadata_url, verify=False)
        except:
            raise OIDCError("Could not load metadata from server", "OIDCMetadataCache.load_metadata")
        metadata = resp.json()
        return OIDCMetadata(vals=metadata)

class OIDCKeystoreCache(SingletonMixin):

    def __init__(self):
        self.keys = {}
        self.keys_lock = threading.Lock()

    def get_key(self, jwks_uri, kid):
        keystore_tuple = self.keys.get(jwks_uri, None)
        if not keystore_tuple:
            with self.keys_lock:
                keystore_tuple = self.keys.get(jwks_uri, None)
                if not keystore_tuple:
                    keystore_tuple = (threading.Lock(), None)
                    self.keys[jwks_uri] = keystore_tuple
        if not keystore_tuple[1]:
            with keystore_tuple[0]:
                keystore_tuple = self.keys[jwks_uri]
                if not keystore_tuple[1]:
                    keystore_tuple = (keystore_tuple[0], self.load_keystore(jwks_uri))
                    self.keys[jwks_uri] = keystore_tuple
        return keystore_tuple[1].get(kid, None)

    def load_keystore(self, jwks_uri):
        resp = None
        try:
            resp = requests.get(url=jwks_uri, verify=False)
        except:
            raise OIDCError("Could not keystore from oidc idp", "OIDCMetadataCache.load_keystore")
        keystore = resp.json()["keys"]
        ret = {}
        for key in keystore:
            kid = key['kid']
            ret[kid] = from_jwk(key)
        return ret