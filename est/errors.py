"""Errors definitions."""

class Error(Exception):
    """Top error class. All errors should derive this class.

    Attributes:
        message (str): Error message.
    """

    def __init__(self, message):
        Exception.__init__(self, message)


class RequestError(Error):
    """Server request error.

    Attributes:
        status (int): Error http status code.
        message (str): Error message.
    """

    status = None
    message = None

    def __init__(self, status, message):
        Error.__init__(self, message)
        self.status = status
        self.message = message

    def __str__(self):
        return "RequestError: status=%s, message=%s" % (
            self.status, self.message)

    def __repr__(self):
        return "RequestError(status=%r, message=%r)" % (
            self.status, self.message)

