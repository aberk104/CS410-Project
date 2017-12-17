from unittest import TestCase
from address_compare.feature_functions import FullAddressFeatures

class TestFullAddressFeatures(TestCase):
    def test_f_contains_street_name_words(self):
        ff = FullAddressFeatures()
        self.assertTrue(ff.f_contains_street_name_words(["a", "street"]))
        self.assertTrue(ff.f_contains_street_name_words(["a", "Street."]))
        self.assertFalse(ff.f_contains_street_name_words(["a", "b"]))