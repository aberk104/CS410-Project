import pandas as pd
from sklearn.metrics import confusion_matrix

DEFAULT_TEST_DATA = './data/compare_train.csv'

def evaluate_comparer(comparer, testing_data = DEFAULT_TEST_DATA):
    '''

    :param comparer: a comparer function that takes two strings and returns true if they represent the same address
    :param df: either a dataframe, or the path to a csv where the first two columns
    :return:
    '''

    if type(testing_data) == str:
        testing_data = pd.read_csv(DEFAULT_TEST_DATA)


    pairs = testing_data.iloc[:, [0,1]]
    result = [comparer(a, b) for i, a, b in pairs.itertuples()]
    return pd.DataFrame(dict(actual = testing_data.iloc[:, 2], predicted = result))

