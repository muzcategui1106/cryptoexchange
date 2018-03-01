class CryptoExchangeException(Exception):
    def __init__(self, message):
        self.message = message


class RestMessengerError(CryptoExchangeException):
    pass

class ExchangeError(CryptoExchangeException):
    pass