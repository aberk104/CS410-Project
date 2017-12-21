import re
from string import punctuation

from address_compare.constants import DIRECTIONS, STREET_TYPES, UNIT_TYPES
from address_compare.parsers import omit_hyphen

DEFAULT_TOKENIZER = omit_hyphen
DEFAULT_LAGS = 0
DEFAULT_LEADS = 1


class FeatureFunctions:
    """
    A base class for objects that hold feature functions.
    """

    def exec_all(self, x, prefix: str=""):
        """
        Applies every feature function to x. Returns a dict where keys are function
        names and values are the values of the features, with an optional prefix.

        :param x: the object on which to apply the feature functions. This might be a single
        token, or it might be a whole sentence.
        :param prefix: The prefix to append to the front of each key.
        :return: A dictionary of feature values suitable for plugging into crfsuite.
        """
        return {prefix + k: getattr(self, k)(x) for k in dir(self) if k.startswith("f_")}

class WordFeatures1(FeatureFunctions):

    def f_is_street_name(self, s: str):
        """

        :param s: string
        :return: true iff s is a street type, i.e. Avenue, Street, etc.
        """
        return s.lower().strip(punctuation) in STREET_TYPES

    def f_is_direction(self, s: str):
        """

        :param s: string
        :return: true if f is a direction
        """
        return s.lower() in DIRECTIONS

    def f_self_tolower(self, s: str):
        """

        :param s: a string
        :return: s in lower case
        """
        return s.lower()

    def f_is_digit(self, s: str):
        """

        :param s: a string
        :return: true if s is a digit
        """
        return s.isdigit()

    def f_has_digit(self, s):
        """

        :param s: string
        :return: true if s contains a digit
        """
        return re.search('\d', s) is not None

    def f_length(self, s: str):
        """

        :param s: a string
        :return: the length of s
        """
        return len(s)

    def f_last_char(self, s: str):
        """

        :param s: a string
        :return: the last character of s
        """
        return s[-1]

    def f_first_char(self, s:str):
        """

        :param s: a string
        :return: the first character of se
        """

        return s[0]


class WordFeatures2(FeatureFunctions):
    """
    This was the best performing WordFeatures object we tried.
    """

    def f_is_street_type_word(self, s: str):
        """

        :param s: a string
        :return: true if f is a street type
        """
        return s.lower().strip(punctuation) in STREET_TYPES

    def f_is_direction(self, s: str):
        """

        :param s: a string
        :return: true if f is a direction
        """
        return s.lower().strip(punctuation) in DIRECTIONS

    def f_is_digit1(self, s: str):
        """

        :param s: s
        :return: true if s is a 1 digit string
        """
        return s.isdigit() and len(s) == 1

    def f_is_digit2(self, s: str):
        """

        :param s: s
        :return: true if s is a 2 digit string
        """
        return s.isdigit() and len(s) == 2

    def f_is_digit3(self, s: str):
        """

        :param s: s
        :return: true if s is a 3 digit string
        """
        return s.isdigit() and len(s) == 3

    def f_is_digit4(self, s: str):
        """

        :param s: s
        :return: true if s is a 4 digit string
        """
        return s.isdigit() and len(s) == 4

    def f_is_digit5(self, s: str):
        """

        :param s: s
        :return: true if s is a 5 digit string or greater
        """
        return s.isdigit() and len(s) >= 5

    def f_has_digit(self, s):
        """

        :param s: s
        :return: true if s contains a digit
        """
        return re.search('\d', s) is not None
    #
    # def f_length(self, s: str):
    #     return len(s)

    def f_pound(self, s: str):
        """

        :param s: a string
        :return: true if f contains a poundsign
        """
        return '#' in s

    def f_unit_type(self, s: str):
        """

        :param s: a string
        :return: true if f contains a unit type
        """
        return s.lower().strip(punctuation) in UNIT_TYPES

    def f_hwy(self, s: str):
        """

        :param s: a string
        :return: true if f is the word highway or hwy
        """

        return s.lower().strip(punctuation) in ['hwy', 'highway']

    def f_county(self, s: str):
        """

        :param s: a string
        :return: true if f is the word county
        """
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

    """
    The FeatureExtractor object tokenizes a string and applies feature functions to it.
    Every AddressTagger object uses a FeatureExtractor object to make its predictions.
    """

    def __init__(self, tokenizer=DEFAULT_TOKENIZER, word_features: FeatureFunctions = WordFeatures2(),
                 sentence_features: FeatureFunctions = FullAddressFeatures(), lags=DEFAULT_LAGS, leads = DEFAULT_LEADS):
        """
        Initialize a FeatureExtractor object.
        :param tokenizer: Function to convert string into tokens. By default this just splits on spaces.
        :param word_features: Function to extract features from individual words.
        :param sentence_features: Function to extract features from the entire sentence.
        :param lags: Number of lags to apply. If this is set to 1 then each token will be
        assigned its own features as well as the features of its immediate predecessor.
        :param leads: Number of leads to apply. If this is set to 1 then each token will
        be assigned its own features as well as the featuers of its immediate successor.
        """
        self.tokenizer = tokenizer
        self.word_features = word_features
        self.sentence_features = sentence_features
        self.lags = lags
        self.leads = leads

    def extract_features_from_string(self, s: str):
        """
        Tokenize a string and extract features from it
        :param s: The string to extract features from
        :return:  A feature set suitable for plugging into a crfsuite tagger or trainer
        """
        token_list = self.tokenizer(s)
        return self.extract_features_from_token_list(token_list)

    def extract_features_from_token_list(self, token_list):
        """
        Does the heavy lifting here -- applies the feature functions to the tokens
        :param token_list: list of tokens
        :return: Feature set suitable for plugging into a crfsuite tagger or trainer.
        """
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