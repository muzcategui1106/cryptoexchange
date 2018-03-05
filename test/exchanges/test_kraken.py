import asynctest as asynctest
from unittest.mock import MagicMock
from cryptoexchange.exchanges.kraken import Kraken
from cryptoexchange.exceptions.exceptions import RestMessengerError
from test.test_utils import TestUtil

kraken_asset_pair_response = {
    "result" : {
        "BTCUSD" : [],
        "ETHUSD": []
    }
}

kraken_symbol_info_response = {
    "result" : {
        "BTCUSD": {
            "a" : 1,
            "b" : 2
        },
        "ETHUSD": {
            "a": 3,
            "b": 4
        }
    }
}



class TestKraken(asynctest.TestCase):
    def setUp(self):
        self.kraken = Kraken()

    async def test_get_all_asset_pairs(self):
        self.kraken.get_json = asynctest.CoroutineMock(return_value=kraken_asset_pair_response)
        actual = await self.kraken.get_all_asset_pairs()
        self.assertListEqual(sorted(actual), sorted(["BTCUSD", "ETHUSD"]))

    async def test_get_all_asset_pairs_returns_empty_list_when_kraken_response_failed(self):
        self.kraken.get_json = asynctest.CoroutineMock(side_effect=RestMessengerError("error"))
        self.assertListEqual(await self.kraken.get_all_asset_pairs(), [])

    async def test_get_all_asset_pairs_returns_emtpy_list_when_kraken_response_is_not_well_structured(self):
        self.kraken.get_json = asynctest.CoroutineMock(return_value={})
        self.assertListEqual(list(await self.kraken.get_all_asset_pairs()), [])

    async def test_get_symbols_info_from_exchange(self):
        self.kraken.get_all_asset_pairs = asynctest.CoroutineMock(return_value=["BTCUSD", "ETHUSD"])
        self.kraken.get_json = asynctest.CoroutineMock(return_value=kraken_symbol_info_response)
        expected = TestUtil.sorted_list_of_es_docs(self.kraken.to_es_doc_list(kraken_symbol_info_response["result"]))
        actual = TestUtil.sorted_list_of_es_docs(await self.kraken.get_symbols_info_as_es_docs())
        self.assertListEqual(sorted(actual), sorted(expected))

    async def test_get_symbols_info_from_exchange_includes_timestmaps(self):
        self.kraken.get_all_asset_pairs = asynctest.CoroutineMock(return_value=["BTCUSD", "ETHUSD"])
        self.kraken.get_json = asynctest.CoroutineMock(return_value=kraken_symbol_info_response)
        actual = await self.kraken.get_symbols_info_as_es_docs()
        self.assertIsNotNone(actual[0].timestamp)