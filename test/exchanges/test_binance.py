import asynctest as asynctest
from cryptoexchange.exchanges.binance import Binance
from cryptoexchange.es.es_doc import EsDoc
from cryptoexchange.exceptions.exceptions import RestMessengerError
from test.test_utils import TestUtil

binance_symbol_info_response = [
    {
        "price":  10,
        "symbol" : "BTCUSD",
    },
    {
        "price": 50,
        "symbol": "ETHUSD",
    },

]

class TestBinance(asynctest.TestCase):
    def setUp(self):
        self.binance = Binance()

    async def test_get_symbols_info_from_exchanges_with_binance_good_response(self):
        async def func():
            return binance_symbol_info_response
        self.binance.get_json = asynctest.CoroutineMock(return_value=binance_symbol_info_response)
        response = await self.binance.get_symbols_info_from_exchange()
        self.assertDictEqual(response[0], binance_symbol_info_response[0])
        self.assertDictEqual(response[1], binance_symbol_info_response[1])

    async def test_get_symbols_info_from_exchanges_with_binance_error(self):
        self.binance.get_json = asynctest.CoroutineMock(side_effect=RestMessengerError("error"))
        response = await self.binance.get_symbols_info_from_exchange()
        self.assertListEqual(response, [])

    def test_to_es_doc_list_returns_empty_if_empty_result_is_passed(self):
        self.assertListEqual(self.binance.to_es_doc_list([]), [])

    def test_to_es_doc_list(self):
        doc_list = TestUtil.sorted_list_of_es_docs(self.binance.to_es_doc_list(binance_symbol_info_response))
        expected = TestUtil.sorted_list_of_es_docs([EsDoc(price=10, symbol="BTCUSD", exchange_name=self.binance.name),
                    EsDoc(price=50, symbol="ETHUSD", exchange_name=self.binance.name)])
        self.assertListEqual(doc_list, expected)

    def test_to_es_doc_includes_timestamps(self):
        doc_list = self.binance.to_es_doc_list(binance_symbol_info_response)
        self.assertIsNotNone(doc_list[0].timestamp)
