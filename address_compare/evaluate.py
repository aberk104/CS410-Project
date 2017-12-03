import pandas as pd
from sklearn.metrics import confusion_matrix
from address_compare.comparers import naive_compare

DEFAULT_TEST_DATA = 'data/compare_train.csv'

def evaluate_comparer(comparer, testing_csv = DEFAULT_TEST_DATA):
    '''

    :param comparer: a comparer function that takes two strings and returns true if they represent the same address
    :param df: the path to a csv where the first two columns
    :return:
    '''
    
    df = pd.read_csv(DEFAULT_TEST_DATA)

    pairs = df.iloc[:, [0,1]]
    result = [comparer(a, b) for i, a, b in pairs.itertuples()]
    return pd.DataFrame(dict(actual = df.iloc[:, 2], predicted = result))

