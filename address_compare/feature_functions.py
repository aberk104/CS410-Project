import re
from collections import OrderedDict

import pandas as pd
from typing import List
from .constants import DIRECTIONS, STREET_TYPES, UNIT_TYPES
from string import punctuation
import pycrfsuite
from .parsers import hyphen_parse


class FeatureFunctionApplicator:

    def exec_all(self, x, prefix=None):
        return {k: getattr(self, k)(x) for k in dir(self) if k.startswith("f_")}

class WordFeatures1(FeatureFunctionApplicator):

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


class WordFeatures2(FeatureFunctionApplicator):
    # after training, this ended up being the better one
    def f_is_street_type_word(self, s: str):
        return s.lower().strip(punctuation) in STREET_TYPES

    def f_is_direction(self, s: str):
        return s.lower() in DIRECTIONS

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

    def f_length(self, s: str):
        return len(s)

    def f_pound(self, s: str):
        return '#' in s

    def f_unit_type(self, s: str):
        return s.lower().strip(punctuation) in UNIT_TYPES

    def f_ends_in_hyphen(self, s: str):
        return s[-1] == '-'


