import unittest
from cryptoexchange.rest.rest_messenger import RestMessenger, RestMessage

"""
TODO 
this test uses an external website to test RestMessenger
we should create a small web server so we dont have this dependency
"""
class TestRestMessenger(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_json_will_return_a_json(self):
        actual = RestMessenger().get_json("https://jsonplaceholder.typicode.com/posts/1")
        self.assertTrue(isinstance(actual, dict))

    def test_get_jsons_will_return_more_than_one_result(self):
        url = "https://jsonplaceholder.typicode.com/posts/1"
        messages = [RestMessage(url), RestMessage(url)]
        actual = RestMessenger().get_jsons(messages)
        self.assertEqual(len(actual), 2)

    def test_errors_in_every_call_will_return_an_empty_list(self):
        url = "https://fcdslmcsdmcsc.com"
        messages = [RestMessage(url), RestMessage(url)]
        actual = RestMessenger().get_jsons(messages)
        self.assertEqual(len(actual), 0)

    def test_errors_in_one_call_will_not_make_other_calls_fail(self):
        bad_url = "https://fcdslmcsdmcsc.com"
        good_url = "https://jsonplaceholder.typicode.com/posts/1"
        messages = [RestMessage(bad_url), RestMessage(good_url)]
        actual = RestMessenger().get_jsons(messages)
        self.assertEqual(len(actual), 1)
        self.assertTrue(isinstance(actual[0], dict))
