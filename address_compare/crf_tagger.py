# creates the tag functions using the trained CRF model
from collections import OrderedDict

import address_compare.feature_functions as ff
import pycrfsuite
from address_compare.parsers import hyphen_parse
import pandas as pd
import pkg_resources
from address_compare.standardizers import standardizer
from string import punctuation

MODEL = pkg_resources.resource_filename('address_compare', 'trained_models/model3')
TOKENIZER = hyphen_parse
FF = ff.WordFeatures2()
DF_ORDER = ["STREET_NUMBER", "PRE_DIRECTION", "STREET_NAME", "STREET_TYPE", "POST_DIRECTION",
            "UNIT_TYPE", "UNIT_NUMBER"]

class AddressTagger(object):

    def __init__(self, model = MODEL, tokenizer: "function" = TOKENIZER, ff: ff.FeatureFunctionApplicator = FF):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model)
        self.tokenizer = tokenizer
        self.ff = ff

    def tag(self, s:str, concat: bool = True, standardize = False):
        tokens = self.tokenizer(s)
        features = [self.ff.exec_all(t) for t in tokens]
        tags = self.tagger.tag(features)
        parsed_address = OrderedDict(UNIT_TYPE=[], UNIT_NUMBER=[], STREET_NUMBER=[], PRE_DIRECTION=[],
                                     STREET_NAME=[], STREET_TYPE=[], POST_DIRECTION=[], UNKNOWN=[])
        for a, b in zip(tokens, tags):
            parsed_address[b].append(a.strip(',-'))
        if standardize:
            parsed_address = standardizer(parsed_address)
        if concat:
            parsed_address = {k: ' '.join(v) for k, v in parsed_address.items()}
        return parsed_address

    def series_to_address_df(self, s: pd.Series, concat = True, standardize = True):
        add_dict = s.apply(self.tag, concat = concat, standardize = standardize)
        return pd.DataFrame.from_records(add_dict)[DF_ORDER]

if __name__ == '__main__':
    add = pd.read_csv('data/sample_data.csv')
    t = AddressTagger()
    a = t.series_to_address_df(add['address'])
    print(a)