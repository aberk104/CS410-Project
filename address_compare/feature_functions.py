import re
import pandas as pd
from typing import List
from .constants import DIRECTIONS, STREET_TYPES
from string import punctuation


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

class SentenceFeatures(FeatureFunctionApplicator):

    def f_length(self, l: List[str]):
        return len(l)

    def f_ends_in_street_type(self, l: List[str]):
        return l[-1].lower() in STREET_TYPES

    def f_ends_in_direction(self, l: List[str]):
        return l[-1].lower() in DIRECTIONS