from unittest.mock import MagicMock

class TestUtil:

    @staticmethod
    def sorted_list_of_es_docs(a):
        TestUtil.strip_time_from_docs(a)
        return sorted(a)

    @staticmethod
    def strip_time_from_docs(a):
        """
        Test if two EsDoc lists are equal. We only test for certian fields for simplicity
        :param a: a list of EsDocs
        :param b: a list of EsDocs
        :return:
        """
        for doc in a:
            doc.timestamp = None