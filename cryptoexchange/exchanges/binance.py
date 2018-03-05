from logging import getLogger
from cryptoexchange.exchanges.exchange import Exchange
from cryptoexchange.exceptions.exceptions import RestMessengerError
from cryptoexchange.es.es_doc import EsDoc

logger = getLogger()


class Binance(Exchange):
    exchange_uri = "https://api.binance.com"
    name = "binance"

    def __init__(self):
        super(self.__class__, self).__init__()

    async def get_symbols_info_from_exchange(self):
        """
        Queries binance for symbol info
        :return: A list of dictionaries with the following keys: "symbol, price"
        """
        logger.debug("Get all symbols info from {}".format(self.name))
        try:
            return await self.get_json(self.exchange_uri + "/api/v3/ticker/price")
        except RestMessengerError as e:
            logger.error("Unable to get all symbols info from {} due to .. {}".format(self.name, e.message))
            return []

    def to_es_doc_list(self, exchange_result):
        """
        Convert a Binance result containing symbols information into EsDocs
        :param exchange_result: a list of dictionaries with the following keys: "symbol, price"
        :return: a list of esDoc objects
        """
        es_docs = []
        timestamp = self.get_current_time()
        for item in exchange_result:
            es_docs.append(EsDoc(symbol=item["symbol"], price=item["price"], timestamp=timestamp,
                                 exchange_name=self.name))
        return es_docs
