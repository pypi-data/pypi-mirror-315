

class APIError(Exception):
    def __init__(self, message: str, status_code: int = None, response_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data