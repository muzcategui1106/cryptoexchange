from abc import ABCMeta, abstractclassmethod
from cryptoexchange.rest.rest_messenger import RestMessenger
from datetime import  datetime

class Exchange(RestMessenger):
    __metaclass__ = ABCMeta

    def get_symbols_info(self):
        """
        Get information about all the symbols as elasticsearch documents
        :return: A list of esDocs
        """
        return self.to_es_doc_list(self.get_symbols_info_from_exchange())

    @abstractclassmethod
    def get_symbols_info_from_exchange(self):
        """
        Get symbol info from exchange
        :return: The information as return by the exchange. See each implementation for their return values
        """
        raise NotImplementedError


    @abstractclassmethod
    def to_es_doc_list(self, exchange_result):
        """
        Convert an exchange result containing symbols information into EsDocs
        :param exchange_result:
        :return: a list of esDoc objects
        """
        return NotImplementedError

    @staticmethod
    def get_current_time():
        """
        Calculate current time
        :return:
        """
        return datetime.now().timestamp()