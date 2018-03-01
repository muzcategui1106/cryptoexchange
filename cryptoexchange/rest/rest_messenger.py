import asyncio
import aiohttp
import json
from logging import getLogger
from json.decoder import JSONDecodeError
from cryptoexchange.exceptions.exceptions import RestMessengerError

logger = getLogger()

class RestMessenger:
    def get_json(self, uri, headers=None):
        """
        Returns only the first result as a json an ignore the others
        :param uri: uri
        :param headers: headers
        :return: a single Json
        """
        message_list = [RestMessage(uri, headers)]
        return self.jsonify_response(self.async_send(message_list)[0])

    def get_jsons(self, message_lists):
        """
        Returns all the results as a list of json
        :param message_lists:  a list of RestMessages
        :return: a list of jsons
        """
        return self.jsonify_response_list(self.async_send(message_lists))

    def async_send(self, message_list):
        """
        send a list of messages over HTTP asynchronously
        :param message_list: a list of RestMessages
        :return: a list of responses
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.__async_send(message_list))
        loop.run_until_complete(future)
        return future.result()

    async def __async_send(self, message_list):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            tasks = []
            for message in message_list:
                tasks.append(asyncio.ensure_future(self.__send(session, message)))
            return await asyncio.gather(*tasks)

    async def __send(self, session, message):
        try:
            async with session.request(message.http_method, message.uri, **message.kwargs) as response:
                return await response.read()
        except aiohttp.ClientError as e:
                logger.error("Error while sending request to uri {} ... {}".format(message.uri, e))
                return None

    @staticmethod
    def jsonify_response_list(responses):
        """
        jsonify a list of response strings
        :param responses:
        :return:
        """
        jsons = []
        for r in responses:
            try:
                jsons.append(RestMessenger.jsonify_response(r))
            except RestMessengerError as e:
                logger.error(e.message)
        return  jsons


    @staticmethod
    def jsonify_response(response):
        """
        Convert a response string to Json
        :param response: a string response
        :return: a json
        :raises: JSONDecodeError, TypeError
        """
        try:
            return json.loads(response)
        except (JSONDecodeError, TypeError):
            raise RestMessengerError("Error while decoding json response {}".format(response))


class RestMessage:
    def __init__(self, uri, headers=None, http_method="get", **kwargs):
        self.uri = uri
        self.headers = headers
        self.kwargs = kwargs
        self.http_method = http_method
