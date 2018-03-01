import unittest
from cryptoexchange.es.es_doc import EsDoc

class TestEsDoc(unittest.TestCase):

    def test_EsDoc_can_be_initialized(self):
        doc = EsDoc(price=1, symbol="BTCUSD")
        self.assertEqual(doc.price, 1)
        self.assertEqual(doc.symbol, "BTCUSD")