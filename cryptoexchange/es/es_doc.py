import hashlib
from json import JSONEncoder


class EsDoc:
    def __init__(self, **kwargs):
        self.symbol = kwargs.get("symbol", None)
        self.price = kwargs.get("price", None)
        self.bid = None
        self.ask = None
        self.market_cap = None
        self.timestamp = kwargs.get("timestamp", None)
        self.exchange_name = kwargs.get("exchange_name", "unknown")

    def doc_hash(self):
        """
        Returns a hash of fields of the doc
        :return: a string
        """
        s = self.exchange_name + self.symbol + str(self.price) + str(self.timestamp)
        return hashlib.md5(s.encode("UTF-8")).hexdigest()

    def __eq__(self, other):
        return self.doc_hash() == other.doc_hash()

    def __lt__(self, other):
        return self.doc_hash() <= other.doc_hash()