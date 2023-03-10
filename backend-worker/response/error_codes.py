from typing import Optional


class ErrorException(Exception):
    successful: bool
    error_code: str
    message: str
    status_code: int

    def __init__(self, successful: bool, error_code: str, message: str, status_code: int):
        self.successful = successful
        self.error_code = error_code
        self.message = message
        self.status_code = status_code


def get_http_exception(error_code: str, message: Optional[str] = None) -> ErrorException:
    responses = filter(lambda element: element.error_code == error_code, ERROR_CODES)
    response = list(responses)[0]
    raise ErrorException(
            successful=response.successful,
            error_code=response.error_code,
            message=message if message else response.message,
            status_code=response.status_code,
        )


ERROR_CODES = [
    ErrorException(
        error_code='03',
        message='Server Error',
        successful=False,
        status_code=500,
    ),
    ErrorException(
        error_code='06',
        message='Invalid data',
        successful=False,
        status_code=400,
    ),
    ErrorException(
        error_code='10',
        message='Unauthorised',
        successful=False,
        status_code=401,
    ),
    ErrorException(
        error_code='IP400',
        message='Missing Input field(s)',
        successful=False,
        status_code=400,
    )
]
