# this file contains parsers for converting address strings to lists
# of tokens
import re
from nltk import tokenize

def naive_parse(s: str, tolower: bool = False) -> list:
    """

    :param s: string to be parsed
    :param tolower: convert to lowercase?
    """
    return [k.lower() for k in s.split()] if tolower else s.split()

def hyphen_parse(s: str, tolower: bool = True) -> list:
    """
    keeps trailing hyphens, i.e. hyphen_parse("A-b") = ["A-", "b"]
    :param s: string to be parsed
    :param tolower: convert to lowercase?
    """
    parts = [re.split('(\w+-)', k) for k in re.split(' |\t', s)]
    return [k for sl in parts for k in sl if k and (k != '-')]