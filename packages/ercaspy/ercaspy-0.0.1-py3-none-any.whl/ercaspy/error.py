class ErcasError(Exception):
    """Base class for exceptions in this module."""

    pass


class ErcasBadRequestError(ErcasError):
    """Exception raised for errors in the request.

    Attributes:
        message -- explanation of the error
    """

    pass


class ErcasUnauthorizedError(ErcasError):
    """Exception raised for errors in the authentication.

    Attributes:
        message -- explanation of the error
    """

    pass


class ErcasForbiddenError(ErcasError):
    """Exception raised for errors in the authorization.

    Attributes:
        message -- explanation of the error
    """

    pass


class ErcasNotFoundError(ErcasError):
    """Exception raised for errors in the resource not found.

    Attributes:
        message -- explanation of the error
    """

    pass


class ErcasUnprocessableError(ErcasError):
    """Exception raised for errors that are not processable.

    Attributes:
        message -- explanation of the error
    """

    pass
