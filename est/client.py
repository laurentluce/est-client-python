"""EST Client.

This is the first object to instantiate to interact with the API.
"""

import base64
import ssl
import subprocess

import OpenSSL.crypto

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
        res = est.request.get(url, verify=self.implicit_trust_anchor_cert_path)

        pem = ssl.DER_cert_to_PEM_cert(base64.b64decode(res.content))

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
        res = est.request.post(url, csr, auth=auth, headers=headers,
            verify=self.implicit_trust_anchor_cert_path)
        pem = self.pkcs7_to_pem(base64.b64decode(res.content))

        return pem

    def simplereenroll(self, csr, cert_path=False):
        """EST /simplereenroll request.

        Args:
            csr (str): Certificate signing request (PEM).

            cert_path (str): Path to valid client certificate for
                authentication.

        Returns:
            str.  Signed certificate (PEM).

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/simplereenroll'
        auth = (self.username, self.password)
        headers = {'Content-Type': 'application/pkcs10'}
        res = est.request.post(url, csr, auth=auth, headers=headers,
                verify=self.implicit_trust_anchor_cert_path,
                cert=cert_path)
        pem = self.pkcs7_to_pem(base64.b64decode(res.content))

        return pem

    def set_basic_auth(self, username, password):
        """Set up HTTP Basic authentication.

        Args:
            username (str).

            password (str).
        """
        self.username = username
        self.password = password

    def create_csr(self, common_name, country, state, city, organization,
        organizational_unit, email_address):
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
        req.get_subject().C = country
        req.get_subject().ST = state
        req.get_subject().L = city
        req.get_subject().O = organization
        req.get_subject().OU = organizational_unit
        req.get_subject().CN = common_name
        req.get_subject().emailAddress = email_address

        req.set_pubkey(key)
        req.sign(key, 'sha256')

        private_key = OpenSSL.crypto.dump_privatekey(
            OpenSSL.crypto.FILETYPE_PEM, key)

        csr = OpenSSL.crypto.dump_certificate_request(
                   OpenSSL.crypto.FILETYPE_PEM, req)

        return private_key, csr

    def pkcs7_to_pem(self, pkcs7):
        stdout, stderr = subprocess.Popen(
            ['openssl', 'pkcs7', '-inform', 'DER', '-outform', 'PEM',
             '-print_certs'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        ).communicate(pkcs7)

        return stdout
