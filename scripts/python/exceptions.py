class RequestException(Exception):
    def __init__(self, message, original):
        super().__init__(message)
        self.message = message
        self.original = original

    def __str__(self):
        return f"{self.message} ({self.original})"
