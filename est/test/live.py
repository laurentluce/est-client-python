import est.client

host = 'testrfc7030.cisco.com'
port = 8443
implicit_trust_anchor_cert_path = 'server.pem'

client = est.client.Client(host, port, implicit_trust_anchor_cert_path)

print client.ca_certs()

username = 'estuser'
password = 'estpwd'

client.set_basic_auth(username, password)

common_name = 'test'
country = 'US'
state = 'Massachusetts'
city = 'Boston'
organization = 'Cisco Systems'
organizational_unit = 'ENG'

key, csr = client.create_csr(common_name, country, state, city, organization,
        organizational_unit)
print key
print csr

client_cert = client.simpleenroll(csr)
print client_cert
with open('client.pem', 'w') as f:
    f.write(client_cert)

client_cert = client.simplereenroll(csr, 'client.pem')
print client_cert

