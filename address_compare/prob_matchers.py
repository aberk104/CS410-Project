import pandas as pd
import re
from editdistance import eval as ed
import pickle
import pkg_resources
from itertools import product

MODEL = pkg_resources.resource_filename('address_compare', 'trained_models/random_forest_1')

ADDRESS_COLS = ["STREET_NUMBER", "PRE_DIRECTION", "STREET_NAME", "STREET_TYPE", "POST_DIRECTION",
                "UNIT_TYPE", "UNIT_NUMBER"]
DIST_COLS = ["STREET_NAME", "STREET_TYPE", "UNIT_NUMBER"]



class MatchClassifier:
    """
    This class handles the binary classifier that determines if two parsed address strings refer to the same address.
    It loads up a previously trained model and makes predictions.

    """
    def __init__(self, model=MODEL):
        """
        Create the Match Classifier

        :param model: path to the previously trained model. The model should be trained using the features applied in features_from_tagged_addresses
        """
        with open(model, 'rb') as f:
            self.model = pickle.load(f)

    def predict_label(self, a1, a2):
        """
        Given tagged addresses in dataframes a1 and a2, determine whether they refer to the same physical address

        :param a1: tagged addresses dataframe
        :param a2: tagged addresses dataframe
        :return: boolean series
        """
        features = features_from_tagged_addresses(a1, a2)
        return self.model.predict(features)

    def predict_prob(self, a1, a2):
        """
        Given tagged addresses in dataframes a1 and a2, provide a probability that they refer to the same
        physical address.

        :param a1: tagged addresses dataframe
        :param a2: tagged addresses dataframe
        :return: numeric series
        """
        features = features_from_tagged_addresses(a1, a2)
        return self.model.predict_proba(features)[:, 1]


def digit_extract(s):
    """
    Given a a string like "34th", return "34"

    :param s: a string
    :return: a string
    """
    re_digit_extract = re.compile('(^\d+$|\d+(?=st|nd|rd|th|ST|ND|RD|TH))')
    d = re_digit_extract.search(s)
    return d.group() if d is not None else ''


def equal_features(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Given tagged addresses in dataframes a1 and a2, return a matrix where entry i,j is True if df1[i,j]==df2[i,j].
    Applies to the columns in ADDRESS_COLS.

    :param df1: tagged address dataframe
    :param df2: tagged addresses dataframe
    :return: dataframe
    """
    out = pd.DataFrame()
    for col in ADDRESS_COLS:
        out[col + '_EQUAL'] = df1[col] == df2[col]
    return out


def number_mod_text(s1, s2):
    """
    Compares a string like "34" to "34th" and returns true if they're the same number

    :param s1: string
    :param s2: string 
    :return: true if the strings refer to the same number.
    """
    if s1 == s2:
        return True
    d1 = digit_extract(s1)
    if d1:
        d2 = digit_extract(s2)
        return d1 == d2
    return False


def number_mod_text_series(s1, s2):
    """
    Applies number_mod_text to each element in two series

    :param s1: series
    :param s2: series
    :return: boolean series
    """
    return pd.concat([s1, s2], 1).apply(lambda x: number_mod_text(x[0], x[1]), 1, raw=True)


def features_from_tagged_addresses(ad1, ad2):
    """
    Applies feature functions to tagged address dataframes.

    :param ad1: tagged addresss dataframe
    :param ad2: tagged addresses dataframe
    :return: 
    """
    features = pd.concat([edit_distance_matrix(ad1, ad2), equal_features(ad1, ad2)], axis=1)
    features['STREET_MOD_TEXT_EQUAL'] = number_mod_text_series(ad1['STREET_NAME'], ad2['STREET_NAME'])
    features['const'] = 1
    return features


def series_ed(s1: pd.Series, s2: pd.Series):
    """
    vectorizes edit distance over two pandas series

    :param s1: series of strings
    :param s2: series of strings
    :return: series of numbers
    """
    return pd.concat([s1, s2], axis=1).apply(lambda x: ed(x[0], x[1]), axis=1, raw=True)


def edit_distance_matrix(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Applies edit distance componentwise to two dataframes at columns in DIST_COLS

    :param df1: tagged addresses datafame
    :param df2: tagged addresses dataframe
    :return: dataframe with boolean entries
    """
    out = pd.DataFrame()
    for col in DIST_COLS:
        out[col + 'DIST'] = series_ed(df1[col], df2[col])
    return out


class ProbMatcher:
    """
    This class performs the probabilistic matching

    """
    def __init__(self, match_classifier: MatchClassifier = MatchClassifier()):
        """
        Inintialize a probabilistic matcher
        :param match_classifier: A match classifier for doing the classification
        """
        self.match_classifier = match_classifier

    def match_probabilities(self, df1: pd.DataFrame, df2: pd.DataFrame, t=0.8):
        """
        Given two dataframes of parsed addresses, returns a dataframe of matching
        indices with a column indicating match probability. Only those records with a score greater than or equal to the threshold will be returned.

        :param df1: a dataframe of address components (i.e. output from AddressTagger)
        :param df2: a dataframe of address components
        :param t: Record matches with a score greater than or equal to this threshold will be returned.
        :return: a dataframe containing 3 columns: the index for the address from the first dataframe, the index for the address from the second dataframe, the model provided score representing the likelihood that 2 addresses are the same
        """
        i1 = list()
        i2 = list()
        for a, b in product(df1.index, df2.index):
            i1.append(a)
            i2.append(b)
        bigdf1 = df1.iloc[i1, :].reset_index()
        bigdf2 = df2.iloc[i2, :].reset_index()

        probs = self.match_classifier.predict_prob(bigdf1, bigdf2)
        out = pd.DataFrame(dict(index_1=bigdf1['index'], index_2=bigdf2['index'], probs=probs))
        return out[probs >= t]
