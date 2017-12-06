# this file contains functions for performing comparisons on address strings and
# lists of address strings.

#import usaddress
#from address_compare import parsers


# def naive_compare(s1: str, s2: str, parser: 'function' = parsers.naive_parse,
#                   **parse_kwargs) -> int:
#     ps1, ps2 = parser(s1, **parse_kwargs), parser(s2, **parse_kwargs)
#     return set(ps1) == set(ps2)
#
# def crf_compare(s1: str, s2: str):
#     pass
#
#
# def list_compare(l1, l2, comparer = naive_compare, threshold = 0):
#     matches = list()
#     for i in l1:
#         i_scores = list()
#         max_score = 0
#         for j in l2:
#             score = comparer(i, j)
#             max_score = score if score > max_score else max_score
#             i_scores.append(score)
#         for n, j in enumerate(l2):
#             if (i_scores[n] == max_score) & (i_scores[n] > threshold) :
#                 matches.append((i, l2.pop(n), i_scores.pop(n)))
#
#     return matches


def exact_compare(address_od1, address_od2):
    '''
    This function takes 2 ordered dictionaries of addresses and returns True if they are identical (exact compare) or False if the values between the 2 dictionaries for at least 1 key do not match
    :param address_od1: an ordered dictionary containing a tagged and standardized address
    :param address_od2: an ordered dictionary containing a tagged and standardized address
    :return: True or False depending on whether or not the 2 ordered dictionaries are identical
    '''

    return (address_od1 == address_od2)


