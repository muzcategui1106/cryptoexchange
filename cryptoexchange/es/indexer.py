from elasticsearch import Elasticsearch, helpers
from cryptoexchange.exchanges import (
    binance,
    kraken
)


class Indexer():
    def __init__(self):
        self.exchanges = [binance.Binance, kraken.Kraken]
        self.__es = None

    @property
    def es(self):
        """
        property field for elasticsearch. Initializes the field only once if it is null
        :return: self.__es
        """
        if self.__es == None:
            self.__es = Elasticsearch(http_auth=('crypto_write', 'password'))
        return self.__es

    def bulk_index(self, docs):
        """
        Indexes objects as a bulk
        :param docs: a list of objects
        :return: None
        """
        helpers.bulk(self.es, actions=self.es_bulk_dictify(docs))

    def index_symbols_info(self):
        """
        Gets symbol info from every exchange and uploads the information to elasticsearch
        :return: None
        """
        for exchange in self.exchanges:
            self.bulk_index(exchange().get_symbols_info())

    @staticmethod
    def es_bulk_dictify(object_list):
        """
        Convert a EsDocList to a list of dictionaries. This is needed to insert the object into elasticsearch
        There must be a better way to serialize this objects
        :param object_list: a list of objects
        :return: a list of dictionaries
        """
        dict_list = []
        for o in object_list:
            d = {
                "op_type": "update",
                "_index": "cryptos",
                "_type": "symbol",
                "_source": o.__dict__
            }
            dict_list.append(d)
        return dict_list


if __name__ == "__main__":
    Indexer().index_symbols_info()
