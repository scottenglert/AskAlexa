import os
import urlparse
import requests
import base64
from OpenSSL import crypto
from datetime import datetime, timedelta

_CACHED_VALIDATOR = {}

def is_timestamp_valid(timestamp, timestamp_tolerance=150):
    '''
    Return True/False if the given timestamp string is within the given
    tolerance.

    :returns: bool
    '''
    request_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    current_time = datetime.utcnow()
    tolerance = timedelta(seconds=timestamp_tolerance)
    return abs(current_time - request_time) < tolerance

def is_request_certified(certificate_url, request_body, signature):
    '''
    Certifies that the request matches the signature and the certificate is valid.
    :returns: bool
    '''
    try:
        validator = _CACHED_VALIDATOR[certificate_url]
    except KeyError:
        validator = CertificateValidator(certificate_url)
        _CACHED_VALIDATOR[certificate_url] = validator

    return validator.is_valid(request_body, signature)

class CertificateValidator(object):
    '''
    Certificate validator class used to validate an Alexa request and check
    the Amazon certificate.
    '''

    SCHEME = 'https'
    HOSTNAME = 's3.amazonaws.com'
    PATH = '/echo.api/'
    PORT = 443
    SAN = 'echo-api.amazon.com'

    def __init__(self, certificate_url):
        self.certificate_url = certificate_url
        self.certificate = None
        self._certificate_checked = False
        self._certificate_valid = False

    @property
    def has_valid_certificate(self):
        if not self._certificate_checked:
            self._validate_certificate()
            self._certificate_checked = True

        return self._certificate_valid

    def _validate_certificate(self):
        '''
        Verify that the signing certificate url is valid and comes from
        Amazon. Return True / False
        '''
        self._certificate_valid = False

        url_parts = urlparse.urlparse(self.certificate_url)

        if url_parts.scheme != self.SCHEME:
            return

        if url_parts.netloc.lower() != self.HOSTNAME:
            return

        norm_path = os.path.normpath(url_parts.path)
        if not norm_path.startswith(self.PATH):
            return

        if url_parts.port is not None and url_parts.port != self.PORT:
            return

        # get the certificate data from amazon and create a certificate object
        certificate_data = requests.get(self.certificate_url)
        amzn_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, str(certificate_data.text))

        if amzn_certificate.has_expired():
            return

        subject = amzn_certificate.get_subject()
        if subject.commonName != self.SAN:
            return

        # certificate is a valid amazon certificate, ok to use
        self.certificate = amzn_certificate
        self._certificate_valid = True

    def is_valid(self, request_body, signature):
        if not self.has_valid_certificate or not self.certificate:
            return False

        # verify that the signature matches the hash of the request body
        decoded_signature = base64.b64decode(signature)
        try:
            return bool(crypto.verify(self.certificate, decoded_signature, request_body, 'sha1') is None)
        except:
            return False


