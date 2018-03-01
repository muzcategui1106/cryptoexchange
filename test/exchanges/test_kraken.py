import unittest
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



class TestKraken(unittest.TestCase):
    def setUp(self):
        self.kraken = Kraken()

    def test_get_all_asset_pairs(self):
        self.kraken.get_json = MagicMock(return_value=kraken_asset_pair_response)
        actual = self.kraken.get_all_asset_pairs()
        self.assertListEqual(sorted(actual), sorted(["BTCUSD", "ETHUSD"]))

    def test_get_all_asset_pairs_returns_empty_list_when_kraken_response_failed(self):
        self.kraken.get_json = MagicMock(side_effect=RestMessengerError("error"))
        self.assertListEqual(self.kraken.get_all_asset_pairs(), [])

    def test_get_all_asset_pairs_returns_emtpy_list_when_kraken_response_is_not_well_structured(self):
        self.kraken.get_json = MagicMock(return_value={})
        self.assertListEqual(list(self.kraken.get_all_asset_pairs()), [])

    def test_get_symbols_info_from_exchange(self):
        self.kraken.get_all_asset_pairs = MagicMock(return_value=["BTCUSD", "ETHUSD"])
        self.kraken.get_json = MagicMock(return_value=kraken_symbol_info_response)
        expected = TestUtil.sorted_list_of_es_docs(self.kraken.to_es_doc_list(kraken_symbol_info_response["result"]))
        actual = TestUtil.sorted_list_of_es_docs(self.kraken.get_symbols_info())
        self.assertListEqual(sorted(actual), sorted(expected))

    def test_get_symbols_info_from_exchange_includes_timestmaps(self):
        self.kraken.get_all_asset_pairs = MagicMock(return_value=["BTCUSD", "ETHUSD"])
        self.kraken.get_json = MagicMock(return_value=kraken_symbol_info_response)
        actual = self.kraken.get_symbols_info()
        self.assertIsNotNone(actual[0].timestamp)