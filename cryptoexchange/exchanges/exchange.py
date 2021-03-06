import asyncio
from abc import ABCMeta, abstractclassmethod
from cryptoexchange.rest.rest_messenger import RestMessenger
from datetime import  datetime

class Exchange(RestMessenger):
    __metaclass__ = ABCMeta

    @classmethod
    def get_symbols_info_from_all_exchanges(cls):
        # TODO this implementation requires the subclasses to be imported in __init__.py there might be a better way
        tasks = []
        async def wrapper():
            for exchange in cls.__subclasses__():
                instance = exchange()
                tasks.append(asyncio.ensure_future(instance.get_symbols_info_as_es_docs()))
            return await asyncio.gather(*tasks)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(wrapper())
        loop.run_until_complete(future)
        return future.result()

    async def get_symbols_info_as_es_docs(self):
        """
        Get information about all the symbols as elasticsearch documents
        :return: A list of esDocs
        """
        return self.to_es_doc_list(await self.get_symbols_info_from_exchange())

    @abstractclassmethod
    async def get_symbols_info_from_exchange(self):
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