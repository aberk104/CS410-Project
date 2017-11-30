from unittest import TestCase
from .parsers import *
from .comparers import *


class TestNaive_parse(TestCase):
    def test_naive_parse(self):
        self.assertEqual(naive_parse("a b c"), ["a", "b", "c"])
        self.assertEqual(naive_parse("A b c", tolower=True), ["a", "b", "c"])

class TestNaive_compare(TestCase):
    def test_naive_parse_no_kwargs(self):
        self.assertTrue(naive_compare("a b c", "b a c", naive_parse))
        self.assertFalse(naive_compare("a b c", "B a c", naive_parse))
    def test_naive_parse_kwargs(self):
        self.assertTrue(naive_compare("a b c", "B A c", naive_parse, tolower = True))

class TestList_compare(TestCase):
    def test_list_compare1(self):
        self.assertEqual(list_compare(['a'], ['a']), [('a', 'a', 1)])
        self.assertEqual(list_compare(['a b'], ['b a']), [('a b', 'b a', 1)])
        self.assertEqual(list_compare(['A'], ['a']), [])
        self.assertEqual(list_compare(["123 345 Fa", "a, b"], ["345 FA 123", "b a,"],
                                      lambda x, y: naive_compare(x, y, naive_parse, tolower=True)),
                         [("123 345 Fa", "345 FA 123", 1), ("a, b", "b a,", 1)])