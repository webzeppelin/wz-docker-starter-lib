import threading
from ..config import OIDCConfig
from ..config import app

class OIDCClient(object):
    def __init__(self, oidc_config = app.oidc_config):
        self.oidc_config = oidc_config

    def load_metadata(self):
        pass

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
                    meta_tuple = (meta_tuple[0], load_metadata)