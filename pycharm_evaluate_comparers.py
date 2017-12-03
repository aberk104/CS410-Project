from address_compare.comparers import *
from address_compare.parsers import *
from address_compare.evaluate import *
import pandas as pd

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