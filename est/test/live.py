import unittest

import OpenSSL.crypto

import est.client

class Test(unittest.TestCase):

    def setUp(self):
        host = 'testrfc7030.cisco.com'
        port = 8443
        implicit_trust_anchor_cert_path = 'server.pem'
        self.client = est.client.Client(host, port,
            implicit_trust_anchor_cert_path)

    def set_auth(self):
        username = 'estuser'
        password = 'estpwd'
        self.client.set_basic_auth(username, password)

    def create_csr(self):
        common_name = 'test'
        organization = 'Cisco Systems'
        email_address = 'test@cisco.com'
        key, csr = self.client.create_csr(common_name,
            organization=organization, email_address=email_address)
        return csr

    def test_cacerts(self):
        ca_certs = self.client.cacerts()
        lines = ca_certs.split('\n')
        self.assertEqual(lines[0], 'subject=/CN=estExampleCA')

    def test_simpleenroll(self):
        self.set_auth()
        csr = self.create_csr()
        client_cert = self.client.simpleenroll(csr)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
            client_cert)
        self.assertEqual(x509.get_subject().CN, 'test')
        self.assertEqual(x509.get_issuer().CN, 'estExampleCA')

    def test_simplereenroll(self):
        self.set_auth()
        csr = self.create_csr()
        client_cert = self.client.simplereenroll(csr)
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
            client_cert)
        self.assertEqual(x509.get_subject().CN, 'test')
        self.assertEqual(x509.get_issuer().CN, 'estExampleCA')

    def test_csrattrs(self):
        self.client.csrattrs()


if __name__ == '__main__':
    unittest.main()

