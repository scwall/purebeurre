from unittest import TestCase

from packages.search_quote import search_quote


class TestSearch_quote(TestCase):
    def test_search_quote(self):
        assert ("'test quote '' '") == search_quote("test quote ' ")
