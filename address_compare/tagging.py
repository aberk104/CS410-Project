'''
The tagging.py module contains the AddressTagger class which is used to parse addresses into their components and tag each component.
'''

# creates the tag functions using the trained CRF model

from collections import OrderedDict
from string import punctuation

import pandas as pd
import pkg_resources
import pycrfsuite

import address_compare.feature_extraction as fe
from address_compare.standardizers import standardizer

DEFAULT_LAGS = 0
DEFAULT_LEADS = 1
MODEL = pkg_resources.resource_filename('address_compare', 'trained_models/model4')
# noinspection PyPep8
FE = fe.FeatureExtractor(lags = DEFAULT_LAGS, leads = DEFAULT_LEADS)
DF_ORDER = ["STREET_NUMBER", "PRE_DIRECTION", "STREET_NAME", "STREET_TYPE", "POST_DIRECTION",
            "UNIT_TYPE", "UNIT_NUMBER"]


class AddressTagger(object):
    """
    An AddressTagger object loads a crfsuite model, stores the feature extractor, and executes tagging
    """
    def __init__(self, model=MODEL, feature_extractor: fe.FeatureExtractor = FE):
        """

        :param model: the path to the trained crfsuite model
        :param feature_extractor: A FeatureExtractor object that goes with the trained model. This should be an instance of the same FeatureExtractor class that was used to train the model.

        """
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model)
        self.feature_extractor = feature_extractor

    def tag(self, s: str, concat: bool = True, standardize=False):
        """
        Tag an address string.

        :param s: string to tag
        :param concat: If true, multiple tokens with the same tag are concatenated into a single string.

                        E.g. STREET_NAME: ["George", "Washington"] becomes STREET_NAME: "George Washington"

        :param standardize: Should tagged tokens be standardized?
        :return: An OrderedDict with tags as keys and tokens as values.
        """

        tokens = self.feature_extractor.tokenizer(s)
        features = self.feature_extractor.extract_features_from_token_list(tokens)
        tags = self.tagger.tag(features)
        parsed_address = OrderedDict(UNIT_TYPE=[], UNIT_NUMBER=[], STREET_NUMBER=[], PRE_DIRECTION=[],
                                     STREET_NAME=[], STREET_TYPE=[], POST_DIRECTION=[], UNKNOWN=[])
        for a, b in zip(tokens, tags):
            parsed_address[b].append(a.strip(punctuation))
        if standardize:
            parsed_address = standardizer(parsed_address)
        if concat:
            parsed_address = {k: ' '.join(v) for k, v in parsed_address.items()}
        return parsed_address

    def series_to_address_df(self, s: pd.Series, concat=True, standardize=True):
        """
        Tag each entry in a Pandas series containing addresses.

        :param s: Pandas series with addresses as values
        :param concat: Passed to self.tag
        :param standardize: Passed to self.tag
        :return: DataFrame with tokens in tag columns.
        """
        add_dict = s.apply(self.tag, concat=concat, standardize=standardize)
        return pd.DataFrame.from_records(add_dict)[DF_ORDER]
