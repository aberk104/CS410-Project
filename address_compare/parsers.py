# this file contains parsers for converting address strings to lists
# of tokens
import re

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
    s = re.sub(' +-', '-', s)
    parts = [re.split('([^\s]+-)', k) for k in re.split(' |\t', s)]
    return [k for sl in parts for k in sl if k and (k != '-')]

def omit_hyphen(s: str) -> list:
    return [k.strip() for k in s.split() if k and (k != '-')]