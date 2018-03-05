from logging import getLogger
from cryptoexchange.exchanges.exchange import Exchange
from cryptoexchange.exceptions.exceptions import RestMessengerError
from cryptoexchange.es.es_doc import EsDoc

logger = getLogger()

class Kraken(Exchange):
    exchange_uri = "https://api.kraken.com"
    name = "kraken"

    def __init__(self):
        super(self.__class__, self).__init__()

    async def get_all_asset_pairs(self):
        """
        Get all the aseet pairs as a list
        :return: A list of assetPairs
        """
        logger.debug("Get all asset pairs from {}".format(self.name))
        try:

            return self.__get_result_section(await self.get_json(self.exchange_uri + "/0/public/AssetPairs")).keys()
        except RestMessengerError as e:
            logger.error("Unable to get all symbols info from {} due to .. {}".format(self.name, e.message))
            return []

    async def get_symbols_info_from_exchange(self):
        """
        Queries kraken for symbol info
        :return: dictionary where the keys are the symbol name and the values are the bid, ask, etc
        """
        # TODO maximum lenght of reuqets might be exceeded due to string concatenation. Fix it
        logger.debug("Get all symbols info from {}".format(self.name))
        asset_pairs = ",".join(await self.get_all_asset_pairs())
        try:
            uri = self.exchange_uri + "/0/public/Ticker?pair=" + asset_pairs
            return self.__get_result_section(await self.get_json(uri))
        except RestMessengerError as e:
            logger.error("Unable to get all symbols info from {} due to .. {}".format(self.name, e.message))
            return {}


    def to_es_doc_list(self, exchange_result):
        """
        Convert a kraken result containing symbols information into EsDocs
        :param exchange_result: a dictionary where the keys are the symbol name and the values are the bid, ask, etc
        :return: a list of esDoc objects
        """
        es_docs = []
        timestamp = self.get_current_time()
        for symbol, info in exchange_result.items():
            try:
                #TODO is the bid the same as the price
                es_docs.append(EsDoc(symbol=symbol, price=info['b'], timestamp =timestamp, exchange_name=self.name))
            except (KeyError, ValueError):
                logger.warning("Error while parsing kraken symbol response {}".format(info))
        return es_docs

    def __get_result_section(self, kraken_result, on_exception=list):
        """
        Kraken result is wrapped inside a "result" key, this method extracts the actual respose
        :param kraken_result:
        :return: Whatever is inside kraken_result["result"]
        """
        try:
            return kraken_result["result"]
        except KeyError:
            logger.error("{} response does not have a result section".format(self.name))
            return {}