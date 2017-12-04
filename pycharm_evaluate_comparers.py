from address_compare.comparers import *
from address_compare.parsers import *
from address_compare.evaluate import *
from collections import Counter
from address_compare.less_naive_parser import *
import pandas as pd

def test_comparers():
    a1 = "123 Fake Street"
    a2 = "123 Street Fake"
    a3 = "123 Fake St."
    print (less_naive_compare(a1, a2))

    print (less_naive_compare(a1, a3))

    test_data = pd.read_csv('address_compare/data/compare_train.csv')

    result = evaluate_comparer(less_naive_compare, test_data)

    # accuracy
    print ((result['actual'] == result['predicted']).mean())

    # precision
    print (result[result['predicted']]['actual'].mean())

    # recall
    print (result[result['actual']]['predicted'].mean())


def test_parsers():
    results = test_tagger_parser()
    tallied_results = Counter(results)
    print(tallied_results)


test_parsers()