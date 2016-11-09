import json
import struct
from jwt.exceptions import InvalidKeyError
from jwt.utils import base64url_decode
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPublicNumbers

def from_jwk(obj):

    if obj.get('kty') != 'RSA':
        raise InvalidKeyError('Not an RSA key')

    # Public key
    numbers = RSAPublicNumbers(
        from_base64url_uint(obj['e']), from_base64url_uint(obj['n'])
    )

    return numbers.public_key(default_backend())

def from_base64url_uint(val):
    if isinstance(val, str):
        val = val.encode('ascii')

    data = base64url_decode(val)

    buf = struct.unpack('%sB' % len(data), data)
    return int(''.join(["%02x" % byte for byte in buf]), 16)