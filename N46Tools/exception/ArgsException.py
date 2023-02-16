from .ApiException import ApiException


class ArgsException(ApiException):
    """
    Arguments Exception.
    """

    def __init__(self, msg: str) -> None:
        """

        @param msg: Error message.
        """
        super().__init__(msg)
        self.msg = msg
