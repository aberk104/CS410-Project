# creates the tag functions using the trained CRF model

from collections import OrderedDict
from string import punctuation

import pandas as pd
import pkg_resources
import pycrfsuite

import address_compare.feature_extraction as fe
from address_compare.parsers import omit_hyphens
from address_compare.standardizers import standardizer

MODEL = pkg_resources.resource_filename('address_compare', 'trained_models/model4')
# noinspection PyPep8
FE = fe.FeatureExtractor(tokenizer=omit_hyphens, lags=0, leads=0)
DF_ORDER = ["STREET_NUMBER", "PRE_DIRECTION", "STREET_NAME", "STREET_TYPE", "POST_DIRECTION",
            "UNIT_TYPE", "UNIT_NUMBER"]


class AddressTagger(object):
    def __init__(self, model=MODEL, feature_extractor: fe.FeatureExtractor = FE):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model)
        self.feature_extractor = feature_extractor

    def tag(self, s: str, concat: bool = True, standardize=False):
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
        add_dict = s.apply(self.tag, concat=concat, standardize=standardize)
        return pd.DataFrame.from_records(add_dict)[DF_ORDER]
