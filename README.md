est-client-python
=================

EST client - RFC 7030

```python
In [2]: import est.client

In [3]: host = 'testrfc7030.cisco.com'

In [4]: port = 8443

In [5]: implicit_trust_anchor_cert_path = '/home/laurent/github/est-client-python/est/test/server.pem'

In [6]: client = est.client.Client(host, port, implicit_trust_anchor_cert_path)

In [7]: ca_certs = client.cacerts()

In [8]: ca_certs
Out[8]: '-----BEGIN CERTIFICATE-----\nMIIBgAYJKoZIhvcNAQcCoIIBcTCCAW0CAQExADALBgkqhkiG9w0BBwGgggFVMIIB\nUTCB+aADAgECAgkA0KHcKQCBESwwCQYHKoZIzj0EATAXMRUwEwYDVQQDEwxlc3RF\neGFtcGxlQ0EwHhcNMTUwNDMwMTcxMDM3WhcNMTYwNDI5MTcxMDM3WjAXMRUwEwYD\nVQQDEwxlc3RFeGFtcGxlQ0EwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATRQg2l\nOw4nCckLhGLxrz6cjb5/xzZRy9TQxFDR8gBerPApG7vRkia6XMK9wERA0kzfB6Ix\n1lm/VvSFrSJlFH43oy8wLTAMBgNVHRMEBTADAQH/MB0GA1UdDgQWBBRa4qhtS8qn\ncBPyzwP4BegORyqI7TAJBgcqhkjOPQQBA0gAMEUCIBzAcT16ZBXzyKdrjo47wUfk\neNJV7oWtuG5XN672X0xrAiEA5tyFJEy9bX5+vpCoPM/1H/IwrQ8+f/I+fUZLJ7Kd\nxGgxAA==\n-----END CERTIFICATE-----\n'

In [9]: username = 'estuser'

In [10]: password = 'estpwd'

In [11]: client.set_basic_auth(username, password)

In [12]: common_name = 'test'

In [13]: country = 'US'

In [14]: state = 'Massachusetts'

In [15]: city = 'Boston'

In [16]: organization = 'Cisco Systems'

In [17]: organizational_unit = 'ENG'

In [20]: private_key, csr = client.create_csr(common_name, country, state, city, organization, organizational_unit)

In [21]: private_key
Out[21]: '-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCkuLMBrYfSVw42\nV8u4s1uvtjF9OpFFHIM93NL5maSaj76xGecWPE3Hqy9FDpNwz7e2aF1gTqZoV3PT\nymMYgDQd7S+EK6AepwTu67qfIhOa8Jbr//Kvq7v0efhNWSWnOo/YlWGp2gnruJP1\neiTSCB7WqGO975m5UdxMRu87jy4l6LoebGgzqQuobHZK7suz1WKVemf4/R12h3ig\nMvlaewfcRCZ8OZL2r5V10SZ8ON+2dMuACl1v3Y1jjkkLK9aL/jUYm2wX+/E8SMII\ncLtkk5fE0FWMc07dkaCsDcHRwj7tAdcVyKv/15t5XnlkG9r1+YQXWUZWx0yiR644\nHQ6Mfc9RAgMBAAECggEAHlWZOZTgb17y0hUnAjOdjeVKhdpUSFrw3GKfQ7IEuyX/\noxO3F8QxOrUOtnPxuRO3rFLZ51N0l8CLJxSdXTS25E/6sSdrjFmLsggdTRL0c1Md\nKAbxhWJl8abIkE37filttiAEZUgvDYbnUIyW3Ur7iuJlw+Os9pDZtf5WLiy2/enr\nHpN5dd+fD3IYbQdbQ1RSbSs6pijG6KROWA8VC8wOoahx0hfRUFUaOixov5z46qJR\ntWBDr++RKYoPH7hhax6ThSAY34KGlvmGD3TFqWTaUYHBr7F5w4Zj/4HLE/sgKQ01\nncqaU0Te5nzyj/NiGFxraruO2u58rOkoyi76PzgpsQKBgQDaNQxvKjOLTs7KRGoc\nl2TOz6gTCKgT92Rxp1rWY8wo8kkfnDsZAbNMr96BVpU/anyPiLRfyBVP1ptc1fMU\nzmOGcPLi2nIsfauEz8Z39Q64x1zbCE7tbXTiOuQXSqW84JLn3Lm0hGd7mnfI5ktK\n79Jd2xbjVJj/5FTHSWjouop8jQKBgQDBQC4wXroZr4TFxf94b1JFeJ6Z44Lv4rg6\ncb1zUJiMHGCONpuUkvV8GVDz1zoGVO/kEp1Ce2cRrudTxDfSEBL6xIOQkQ9gd8QO\nIe4YScXpRRn71RTNQVvxVI2UmZp1RottqfDSqXZmQ30ZIRnYzkADh8W3DwyEtdl/\nSVLXkTRm1QKBgEshes+Hw0mS7+Z62eJQSjhfDWrITz7Yrm/nhIJOyEvM6FqG6143\n1Klx4HW9/xNfsdWl5x0XgicEKGg1jkW6rk/q8eYj+q3Q805+T8Kb0N7UXedYm/xp\n9JW0Wzad0CURWeOVfydlc0/+poG4sXHy0wbX2bCaPzfUQVCAuStwlyA9AoGBALrX\n1tClhcE31mNxoCNNXnoUuSOIuRw+VGkNd2J61kMBXMmjOqFXxUmLIJ3hxhRBIv+c\nj7eroGeUd8yhtma/a9pRDfNEjV1z7nbLj2ykR1nWmdzGlCovuzmFyq2WJaSl5EDP\nQiwr9HHDZrxZKKhaIcJID32Ca1QUjolm11Xc6pFRAoGBAJ7NyW+Y8BonxLOBUe2x\nMe7m819l2ci6UN9O8n0N9RSl4JY0LxxpHd6s/T4jVdGNpc978CADY4w4snR6mn9e\nT2qPUd2T6eWEP+q+uRkNmejo3xSZEzJxVqCaa8qORvk2uL31RfngtMXXtirwO17Z\nONfLXNuAJTTpogvpFY3SsJPC\n-----END PRIVATE KEY-----\n'

In [22]: csr
Out[22]: '-----BEGIN CERTIFICATE REQUEST-----\nMIICsDCCAZgCAQAwazELMAkGA1UEBhMCVVMxFjAUBgNVBAgTDU1hc3NhY2h1c2V0\ndHMxDzANBgNVBAcTBkJvc3RvbjEWMBQGA1UEChMNQ2lzY28gU3lzdGVtczEMMAoG\nA1UECxMDRU5HMQ0wCwYDVQQDEwR0ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A\nMIIBCgKCAQEApLizAa2H0lcONlfLuLNbr7YxfTqRRRyDPdzS+Zmkmo++sRnnFjxN\nx6svRQ6TcM+3tmhdYE6maFdz08pjGIA0He0vhCugHqcE7uu6nyITmvCW6//yr6u7\n9Hn4TVklpzqP2JVhqdoJ67iT9Xok0gge1qhjve+ZuVHcTEbvO48uJei6HmxoM6kL\nqGx2Su7Ls9VilXpn+P0ddod4oDL5WnsH3EQmfDmS9q+VddEmfDjftnTLgApdb92N\nY45JCyvWi/41GJtsF/vxPEjCCHC7ZJOXxNBVjHNO3ZGgrA3B0cI+7QHXFcir/9eb\neV55ZBva9fmEF1lGVsdMokeuOB0OjH3PUQIDAQABoAAwDQYJKoZIhvcNAQELBQAD\nggEBAEWgkXHgiantuNuBUAAXez/9mm1W9+oM1pjXRTDfriyiwXeCJwFxbyXfyJG5\nx0Tqyp/3Cvwv9rt7bINqbFw/Jv7y4ksTeJKYbdLj7jBuiaUj41oe+zXUcncgOvyV\nv4VYlYBaTyUK3UcCEdwVF6vKGhCVWr1+zHqpy9Mlf4SYutRcJkHT3+gEwDG6QGyr\n8GYCucSp+mdZ3pJBsPFK6gd0zAOPrXuZZApib4VhZznSg4cMG+Gh+rnkbVkj4M1x\ndkT32FfdWJT2q4oC1HLZTpKjLXMOKMl/O6uI4L5MxbPHMSDRSWInFTEJ2ne+B/14\nMC+iDR8F5z5GVZCWQEcqSR/RI5c=\n-----END CERTIFICATE REQUEST-----\n'

In [23]: client_cert = client.simpleenroll(csr)

In [24]: client_cert
Out[24]: 'subject=/CN=test\nissuer=/CN=estExampleCA\n-----BEGIN CERTIFICATE-----\nMIICOTCCAeCgAwIBAgICAIcwCQYHKoZIzj0EATAXMRUwEwYDVQQDEwxlc3RFeGFt\ncGxlQ0EwHhcNMTUwODA2MDMzNTMyWhcNMTYwODA1MDMzNTMyWjAPMQ0wCwYDVQQD\nEwR0ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApLizAa2H0lcO\nNlfLuLNbr7YxfTqRRRyDPdzS+Zmkmo++sRnnFjxNx6svRQ6TcM+3tmhdYE6maFdz\n08pjGIA0He0vhCugHqcE7uu6nyITmvCW6//yr6u79Hn4TVklpzqP2JVhqdoJ67iT\n9Xok0gge1qhjve+ZuVHcTEbvO48uJei6HmxoM6kLqGx2Su7Ls9VilXpn+P0ddod4\noDL5WnsH3EQmfDmS9q+VddEmfDjftnTLgApdb92NY45JCyvWi/41GJtsF/vxPEjC\nCHC7ZJOXxNBVjHNO3ZGgrA3B0cI+7QHXFcir/9ebeV55ZBva9fmEF1lGVsdMokeu\nOB0OjH3PUQIDAQABo1owWDAJBgNVHRMEAjAAMAsGA1UdDwQEAwIHgDAdBgNVHQ4E\nFgQUgfrNpRzVzEqVXU2Ck8/5OWHl7E4wHwYDVR0jBBgwFoAUWuKobUvKp3AT8s8D\n+AXoDkcqiO0wCQYHKoZIzj0EAQNIADBFAiAqmLCPDGc121xBrNK9bT0nNgIWTfci\noOiwaot2blxN2gIhAKG/iF1asQmMAo5aduY7EM41+xE/u3fHW3yK2GF7P4jf\n-----END CERTIFICATE-----\n\n'

In [25]: client_cert = client.simplereenroll(csr)

In [26]: client_cert
Out[26]: 'subject=/CN=test\nissuer=/CN=estExampleCA\n-----BEGIN CERTIFICATE-----\nMIICOTCCAeCgAwIBAgICAIgwCQYHKoZIzj0EATAXMRUwEwYDVQQDEwxlc3RFeGFt\ncGxlQ0EwHhcNMTUwODA2MDMzNzM3WhcNMTYwODA1MDMzNzM3WjAPMQ0wCwYDVQQD\nEwR0ZXN0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApLizAa2H0lcO\nNlfLuLNbr7YxfTqRRRyDPdzS+Zmkmo++sRnnFjxNx6svRQ6TcM+3tmhdYE6maFdz\n08pjGIA0He0vhCugHqcE7uu6nyITmvCW6//yr6u79Hn4TVklpzqP2JVhqdoJ67iT\n9Xok0gge1qhjve+ZuVHcTEbvO48uJei6HmxoM6kLqGx2Su7Ls9VilXpn+P0ddod4\noDL5WnsH3EQmfDmS9q+VddEmfDjftnTLgApdb92NY45JCyvWi/41GJtsF/vxPEjC\nCHC7ZJOXxNBVjHNO3ZGgrA3B0cI+7QHXFcir/9ebeV55ZBva9fmEF1lGVsdMokeu\nOB0OjH3PUQIDAQABo1owWDAJBgNVHRMEAjAAMAsGA1UdDwQEAwIHgDAdBgNVHQ4E\nFgQUgfrNpRzVzEqVXU2Ck8/5OWHl7E4wHwYDVR0jBBgwFoAUWuKobUvKp3AT8s8D\n+AXoDkcqiO0wCQYHKoZIzj0EAQNIADBFAiA9b2UfT10MKGRchJhp2vAKGjjJIQ8Q\niL1tJ25uTtDXRwIhAO/gUL+Dza0tk6PSuNiPxqnlmm+6IMZdmwgDTD/gYfTG\n-----END CERTIFICATE-----\n\n'
```
