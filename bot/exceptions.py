class BotBaseException(Exception):
    """Base exception for all custom Trading Bot errors."""
    pass

class BotValidationError(BotBaseException):
    """Raised when user input fails validation."""
    pass

class BotNetworkError(BotBaseException):
    """Raised when max network retries are exceeded."""
    pass

class BotAPIError(BotBaseException):
    """Raised when the Binance API rejects a request."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code
