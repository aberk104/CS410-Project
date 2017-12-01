# this file contains parsers for converting address strings to lists
# of tokens

def naive_parse(s: str, tolower: bool = False) -> list:
    """

    :param s: string to be parsed
    :param tolower: convert to lowercase?
    """
    return [k.lower() for k in s.split()] if tolower else s.split()

def hyphen_parse(s: str, tolower: bool = False) -> list:
    """

    :param s: string to be parsed
    :param tolower: convert to lowercase?
    """
    s = s.replace("-", " - ")
    return [k.lower() for k in s.split()] if tolower else s.split()