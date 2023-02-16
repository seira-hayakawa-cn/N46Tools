class ApiException(Exception):
    """
    Base API Exception Class.
    """

    def __init__(self, msg: str = "An error occurred."):
        """

        @param msg: Error message.
        """
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg
