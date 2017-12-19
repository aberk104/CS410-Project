import re
from collections import OrderedDict

import pandas as pd
from typing import List
from address_compare.constants import DIRECTIONS, STREET_TYPES, UNIT_TYPES
from string import punctuation
import pycrfsuite
from address_compare.parsers import omit_hyphen

DEFAULT_TOKENIZER = omit_hyphen
DEFAULT_LAGS = 0
DEFAULT_LEADS = 1


class FeatureFunctions:

    def exec_all(self, x, prefix: str=""):
        return {prefix + k: getattr(self, k)(x) for k in dir(self) if k.startswith("f_")}

class WordFeatures1(FeatureFunctions):

    def f_is_street_name(self, s: str):
        return s.lower().strip(punctuation) in STREET_TYPES

    def f_is_direction(self, s: str):
        return s.lower() in DIRECTIONS

    def f_self_tolower(self, s: str):
        return s.lower()

    def f_is_digit(self, s: str):
        return s.isdigit()

    def f_has_digit(self, s):
        return re.search('\d', s) is not None

    def f_length(self, s: str):
        return len(s)

    def f_last_char(self, s: str):
        return s[-1]

    def f_first_char(self, s:str):
        return s[0]


class WordFeatures2(FeatureFunctions):
    # after training, this ended up being the better one
    def f_is_street_type_word(self, s: str):
        return s.lower().strip(punctuation) in STREET_TYPES

    def f_is_direction(self, s: str):
        return s.lower().strip(punctuation) in DIRECTIONS

    def f_is_digit1(self, s: str):
        return s.isdigit() and len(s) == 1

    def f_is_digit2(self, s: str):
        return s.isdigit() and len(s) == 2

    def f_is_digit3(self, s: str):
        return s.isdigit() and len(s) == 3

    def f_is_digit4(self, s: str):
        return s.isdigit() and len(s) == 4

    def f_is_digit5(self, s: str):
        return s.isdigit() and len(s) >= 5

    def f_has_digit(self, s):
        return re.search('\d', s) is not None
    #
    # def f_length(self, s: str):
    #     return len(s)

    def f_pound(self, s: str):
        return '#' in s

    def f_unit_type(self, s: str):
        return s.lower().strip(punctuation) in UNIT_TYPES

    def f_hwy(self, s: str):
        return s.lower().strip(punctuation) in ['hwy', 'highway']

    def f_county(self, s: str):
        return s.lower() == 'county'

    #
    # def f_ends_in_hyphen(self, s: str):
    #     return s[-1] == '-'
    #
    # def f_self(self, s):
    #     return s.lower()

class FullAddressFeatures(FeatureFunctions):
    """
    Feature functions for a whole tokenized address
    """

    # def f_length(self, l):
    #     return len(l)

    # def f_cty_rd(self, l):
    #     for j, w in enumerate(l[:-1]):
    #         if w.lower() == 'county':
    #             if l[j+1].lower() == 'road':
    #                 return True
    #     return False


    # def f_contains_highway(self, l):
    #     return any([s.lower() in ['hwy', 'highway', 'county'] for s in l])

class FeatureExtractor(object):

    def __init__(self, tokenizer=DEFAULT_TOKENIZER, word_features: FeatureFunctions = WordFeatures2(),
                 sentence_features: FeatureFunctions = FullAddressFeatures(), lags=DEFAULT_LAGS, leads = DEFAULT_LEADS):
        self.tokenizer = tokenizer
        self.word_features = word_features
        self.sentence_features = sentence_features
        self.lags = lags
        self.leads = leads

    def extract_features_from_string(self, s: str):
        token_list = self.tokenizer(s)
        return self.extract_features_from_token_list(token_list)

    def extract_features_from_token_list(self, token_list):
        n = len(token_list)
        sentence_features = self.sentence_features.exec_all(token_list,
                                                            prefix='full_') if self.sentence_features else dict()
        token_features = []
        for i, t in enumerate(token_list):
            word_features = self.word_features.exec_all(t, prefix='self_')
            word_features.update(sentence_features)
            for j in range(self.lags):
                if i > j:
                    word_features.update(self.word_features.exec_all(token_list[i - j - 1], prefix='lag{}_'.format(j+1)))
            for j in range(self.leads):
                if i + j + 1 < n:
                    word_features.update(self.word_features.exec_all(token_list[i + j + 1], prefix='lead{}_'.format(j+1)))

            token_features.append(word_features)
        return token_features