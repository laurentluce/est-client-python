"""EST Client.

This is the first object to instantiate to interact with the API.
"""

import base64
import ssl
import subprocess

import OpenSSL.crypto

import asn1crypto.core

import est.errors
import est.request

class Client(object):
    """API client.

    Attributes:
        uri (str): URI prefix to use for requests.

        url_prefix (str): URL prefix to use for requests.  scheme://host:port
    """
    url_prefix = None
    username = None
    password = None
    implicit_trust_anchor_cert_path = None

    def __init__(self, host, port, implicit_trust_anchor_cert_path):
        """Initialize the client to interact with the EST server.

        Args:
            host (str): EST server hostname.

            port (int): EST server port number.

            implicit_trust_anchor_cert_path (str):
                EST server implicit trust anchor certificate path.
        """
        self.url_prefix = 'https://%s:%s/.well-known/est' % (host, port)
        self.implicit_trust_anchor_cert_path = implicit_trust_anchor_cert_path

    def cacerts(self):
        """EST /cacerts request.

        Args:
            None

        Returns:
            str.  CA certificates (PEM).

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/cacerts'
        content = est.request.get(url,
            verify=self.implicit_trust_anchor_cert_path)

        pem = self.pkcs7_to_pem(content)

        return pem

    def simpleenroll(self, csr):
        """EST /simpleenroll request.

        Args:
            csr (str): Certificate signing request (PEM).

        Returns:
            str.  Signed certificate (PEM).

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/simpleenroll'
        auth = (self.username, self.password)
        headers = {'Content-Type': 'application/pkcs10'}
        content = est.request.post(url, csr, auth=auth, headers=headers,
            verify=self.implicit_trust_anchor_cert_path)
        pem = self.pkcs7_to_pem(content)

        return pem

    def simplereenroll(self, csr, cert=False):
        """EST /simplereenroll request.

        Args:
            csr (str): Certificate signing request (PEM).

            cert (tuple): Client cert path and private key path.

        Returns:
            str.  Signed certificate (PEM).

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/simplereenroll'
        auth = (self.username, self.password)
        headers = {'Content-Type': 'application/pkcs10'}
        content = est.request.post(url, csr, auth=auth, headers=headers,
            verify=self.implicit_trust_anchor_cert_path,
            cert=cert)
        pem = self.pkcs7_to_pem(content)

        return pem

    def csrattrs(self):
        """EST /csrattrs request.

        Returns:
            OrderedDict.  Example:
                OrderedDict([(u'0', u'1.3.6.1.1.1.1.22'),
                             (u'1', u'1.2.840.113549.1.9.1'),
                             (u'2', u'1.3.132.0.34'),
                             (u'3', u'2.16.840.1.101.3.4.2.2')])

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/csrattrs'
        content = est.request.get(url,
            verify=self.implicit_trust_anchor_cert_path)

        parsed = asn1crypto.core.Sequence.load(content)
        return parsed.native

    def set_basic_auth(self, username, password):
        """Set up HTTP Basic authentication.

        Args:
            username (str).

            password (str).
        """
        self.username = username
        self.password = password

    def create_csr(self, common_name, country=None, state=None, city=None,
                   organization=None, organizational_unit=None,
                   email_address=None):
        """
        Args:
            common_name (str).

            country (str).

            state (str).

            city (str).

            organization (str).

            organizational_unit (str).

            email_address (str).

        Returns:
            (str, str).  Tuple containing private key and certificate
            signing request (PEM).
        """
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

        req = OpenSSL.crypto.X509Req()
        req.get_subject().CN = common_name
        if country:
            req.get_subject().C = country
        if state:
            req.get_subject().ST = state
        if city:
            req.get_subject().L = city
        if organization:
            req.get_subject().O = organization
        if organizational_unit:
            req.get_subject().OU = organizational_unit
        if email_address:
            req.get_subject().emailAddress = email_address

        req.set_pubkey(key)
        req.sign(key, 'sha256')

        private_key = OpenSSL.crypto.dump_privatekey(
            OpenSSL.crypto.FILETYPE_PEM, key)

        csr = OpenSSL.crypto.dump_certificate_request(
                   OpenSSL.crypto.FILETYPE_PEM, req)

        return private_key, csr

    def pkcs7_to_pem(self, pkcs7):
        inform = None
        for filetype in (OpenSSL.crypto.FILETYPE_PEM,
                         OpenSSL.crypto.FILETYPE_ASN1):
            try:
                OpenSSL.crypto.load_pkcs7_data(filetype, pkcs7)
                if filetype == OpenSSL.crypto.FILETYPE_PEM:
                    inform = 'PEM'
                else:
                    inform = 'DER'
                break
            except OpenSSL.crypto.Error:
                pass

        if not inform:
            raise est.errors.Error('Invalid PKCS7 data type')

        stdout, stderr = subprocess.Popen(
            ['openssl', 'pkcs7', '-inform', inform, '-outform', 'PEM',
             '-print_certs'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        ).communicate(pkcs7)

        return stdout
