class AmazonError(Exception):
    """The base exception class for all Amazon errors"""


class LoginError(AmazonError):
    pass


class NotFoundError(AmazonError):
    pass
