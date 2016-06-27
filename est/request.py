"""HTTP requests to server."""

import base64
import time

import requests
import requests.auth
import requests.exceptions

import est.errors

def get(url, params=None, headers=None, retries=3, timeout=10, verify=False,
        cert=False):
    """GET from server.

    Args:
        url (str): Request URL.

    Kwargs:
        params (dict): Request parameters.

        headers (dict): Request headers.

    Returns:
        str: HTTP response.
    """
    request_params = params
    if request_params is None:
        request_params = {}


    res = send(requests.get, url, params=request_params, headers=headers,
        retries=retries, timeout=timeout, verify=verify, cert=cert)

    return res

def post(url, data, headers=None, auth=None, retries=3, timeout=10,
         verify=False, cert=False):
    """POST to server.

    Args:
        url (str): Request URL.

        data: POST data.

        auth (tuple): Authentication username and password.

    Kwargs:
        headers (dict): Request headers.

    Returns:
        str: Server response.
    """
    return send(requests.post, url, data=data, headers=headers, auth=auth,
        retries=retries, timeout=timeout, verify=verify, cert=cert)

def send(method, url, params=None, data=None, headers=None, auth=None,
        retries=3, timeout=10, verify=False, cert=False):
    """Send request to server.

    Args:
        method (method): Requests library method to call.

        url (str): Request URL.

        auth (tuple): Authentication username and password.

    Kwargs:
        params (dict): Request parameters.

        data (str): Request body data.

        headers (dict): Request headers.

    Returns:
        str: Server response.
    """
    request_params = params
    if request_params is None:
        request_params = {}

    request_data = data
    if request_data is None:
        request_data = {}

    if headers:
        request_headers = headers
    else:
        request_headers = {}

    if auth:
        auth = requests.auth.HTTPBasicAuth(*auth)

    message = None
    while retries:
        try:
            res = method(url, params=request_params, data=request_data,
                headers=request_headers,
                timeout=timeout, verify=verify, auth=auth, cert=cert)
            message = res.text
            if res.status_code == 200:
                try:
                    if (res.headers['Content-Transfer-Encoding'] == 'base64'
                        and not res.content.startswith(b'-----BEGIN')):
                        return base64.b64decode(res.content)
                except KeyError:
                    pass
                return res.content
            elif res.status_code in (400, 401, 403, 404, 413, 202):
                break
        except (requests.exceptions.RequestException) as exception:
            message = str(exception)
            res = None

        time.sleep(1)
        retries -= 1

    raise_request_error(res, message)

def raise_request_error(res, message):
    """Raise a RequestError exception.

    Args:
        res (Requests response): HTTP response.

        message (str): Request error message.

    Raises:
        est.errors.RequestError
    """
    if res is not None:
        status = res.status_code
    else:
        status = None

    if status == 202:
        raise est.errors.TryLater(int(res.headers['retry-after']), message)
    else:
        raise est.errors.RequestError(status, message)
