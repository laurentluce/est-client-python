"""EST Client.

This is the first object to instantiate to interact with the API.
"""

import base64
import ssl

import OpenSSL.crypto

import est.request

CA_CERTS_PATH = '/tmp/ca_certs.pem'

class Client(object):
    """API client.

    Attributes:
        uri (str): URI prefix to use for requests.
        
        url_prefix (str): URL prefix to use for requests.  scheme://host:port
    """
    url_prefix = None
    username = None
    password = None

    def __init__(self, host, port, ca_certs_path):
        """Initialize the client to interact with the EST server.

        Args:
            host (str): EST server hostname.

            port (int): EST server port number.

            ca_certs (str): EST server CA certificates path (PEM).
        """
        self.url_prefix = 'https://%s:%s/.well-known/est' % (host, port)
        self.ca_certs_path = ca_certs_path

    def ca_certs(self):
        """Get CA certificates from the server.

        Args:
            None

        Returns:
            str.  CA certificates (PEM).

        Raises:
            est.errors.RequestError
        """
        url = self.url_prefix + '/cacerts'
        res = est.request.get(url, verify=self.ca_certs_path)

        # TODO: Use openssl to convert pkcs7 DER to PEM
        pem = ssl.DER_cert_to_PEM_cert(base64.b64decode(res.content))
        with open(CA_CERTS_PATH, 'w+') as ca_certs_path:
            ca_certs_path.write(pem)

        self.ca_certs_path = CA_CERTS_PATH

        return pem

    def simpleenroll(self, csr):
        url = self.url_prefix + '/simpleenroll'
        res = est.request.post(url, verify=self.ca_certs_path)
        
        return res

    def set_basic_auth(self, username, password):
        self.username = username
        self.password = password

    def create_csr(self, common_name, country, state, city, organization,
        organizational_unit, serial_number, valid_days):
        """
        """
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

        cert = OpenSSL.crypto.X509()
        cert.get_subject().C = country
        cert.get_subject().ST = state
        cert.get_subject().L = city
        cert.get_subject().O = organization
        cert.get_subject().OU = organizational_unit
        cert.get_subject().CN = common_name

        cert.set_serial_number(serial_number)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(valid_days * 24 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.sign(key, 'sha1')

        return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM,
            cert)


