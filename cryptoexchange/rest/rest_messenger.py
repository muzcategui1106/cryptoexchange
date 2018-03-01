import json
from json.decoder import JSONDecodeError
from requests import (
    Session,
    RequestException
)
from cryptoexchange.exceptions.exceptions import RestMessengerError

class RestMessenger:
    def get_json(self, uri, headers=None):
            return self.jsonify_response(self.__send(uri, headers=headers))

    def jsonify_response(self, response):
        try:
            return json.loads(response.text)
        except (JSONDecodeError, TypeError):
            raise RestMessengerError("Error while decoding json response {}".format(response))

    def __send(self, uri, http_method="get", **kwargs):
        try:
            return Session().request(http_method, uri, **kwargs)
        except RequestException as e:
            raise RestMessengerError("Error while sending request to uri {} ...".format(uri))



