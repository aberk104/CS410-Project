from unittest import TestCase
import parsers as parse
import comparers as comp


class TestNaive_parse(TestCase):
    def test_naive_parse(self):
        self.assertEqual(parse.naive_parse("a b c"), ["a", "b", "c"])
        self.assertEqual(parse.naive_parse("A b c", tolower=True), ["a", "b", "c"])

class TestNaive_compare(TestCase):
    def test_naive_parse_no_kwargs(self):
        self.assertTrue(comp.naive_compare("a b c", "b a c", parse.naive_parse))
        self.assertFalse(comp.naive_compare("a b c", "B a c", parse.naive_parse))
    def test_naive_parse_kwargs(self):
        self.assertTrue(comp.naive_compare("a b c", "B A c", parse.naive_parse, tolower = True))

class TestList_compare(TestCase):
    def test_list_compare1(self):
        self.assertEqual(comp.list_compare(['a'], ['a']), [('a', 'a', 1)])
        self.assertEqual(comp.list_compare(['a b'], ['b a']), [('a b', 'b a', 1)])
        self.assertEqual(comp.list_compare(['A'], ['a']), [])
        self.assertEqual(comp.list_compare(["123 345 Fa", "a, b"], ["345 FA 123", "b a,"],
                                      lambda x, y: comp.naive_compare(x, y, parse.naive_parse, tolower=True)),
                         [("123 345 Fa", "345 FA 123", 1), ("a, b", "b a,", 1)])