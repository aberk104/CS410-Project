'''
The matcher.py file contains a match function to compare 2 lists of addresses.
It calls the separate exact and learning compare comparers in order to find a matching address in list 2 for each address in list 1
'''

from address_compare.comparers import exact_compare

cols_to_join_on = ['UNIT_TYPE','UNIT_NUMBER','STREET_NUMBER','PRE_DIRECTION','STREET_NAME','STREET_TYPE','POST_DIRECTION','CITY','STATE','ZIP_CODE','UNKNOWN']

# def match(address_list_1: list, address_list_2: list, compare_function):
#     '''
#     The match function takes 2 lists of addresses and passes them to a defined compare function.
#     The compare function returns a true/false indicating whether or not an address in list 1 is a match to an address in list 2.
#     The record IDs for the matching addresses are added to the matched_pairs list as a tuple.
#     :param address_list_1: this is the first list of addresses
#     :param address_list_2: this is the second list of addresses
#     :param compare_function: the function that will be used to find matching addresses between the 2 lists
#     :return: matched_pairs (a list of tuples containing record IDs from list 1 and list 2 of matching addresses), unmatched_addresses (record IDs for addresses in 1 list that cannot be found in the other list; if in address list 1, a tuple where NA is the second value. if in address list 2, a tuple where NA is the first value)
#     '''
#
#
#     matched_pairs = list()
#     address_list_1_copy = address_list_1.copy()
#
#     address1_index = 0
#
#     for address1 in address_list_1:
#         address2_index = 0
#         for address2 in address_list_2:
#             if compare_function(address1, address2):
#                 matched_pairs.append((address1, address2)) #this will get changed to record IDs instead of the full orderedDict once record IDs become available
#                 address_list_2.pop(address2_index)
#                 address_list_1_copy.pop(address1_index)
#                 break
#             address2_index += 1
#         address1_index += 1
#
#     unmatched_addresses = list()
#     for item in address_list_1_copy:
#         unmatched_addresses.append((item, "NA")) #this will eventually get changed to Record IDs instead of the full orderedDict
#
#     for item in address_list_2:
#         unmatched_addresses.append(("NA", item)) #this will eventually get changed to Record IDs instead of the full orderedDict
#
#     return matched_pairs, unmatched_addresses



def exact_matcher(address_dataframe_1, address_dataframe_2, join_on_cols = cols_to_join_on):
    exact_matches = address_dataframe_1.merge(address_dataframe_2, on=join_on_cols, suffixes=('_list_1','_list_2'))
    return exact_matches

