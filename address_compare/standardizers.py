'''
The standardizers.py file contains functions to help standardize tagged strings of addresses
'''

from collections import OrderedDict



#the below function will sort the list of ordered dictionaries to attempt to make the matching/compare functions more efficient/quicker
def sorter(list_ordered_dict):
    pass





def standardizer(ordered_dict, nested_reference_dictionary = nested_ref_dt_dict):
    '''
    This function is used to standardize the tagged address components after the CRF tagger is used.
    It:
        - changes all values to ALL CAPS
        - removes orphan hyphens and commas
        - removes extra white space at the beginning or end of the word
        - converts short form street types/unit types/directionals to their long form versions
        - removes commas, #, and hyphens that are the first or last letter of a word
    :param ordered_dict: an ordered dictionary after the CRF tagger has been used
    :param nested_reference_dictionary: a nested dictionary where the first keys are the ordered dictionary tags that utilize reference data and the second keys are the short form/abbreviated versions
    :return std_ordered_dict: a new ordered dictionary that has been standardized
    '''

    std_ordered_dict = OrderedDict()

    for key in ordered_dict.keys():
        standardized_list = list()

        for item in ordered_dict[key]:
            item = item.strip()
            item = item.strip(",")
            item = item.strip("-")
            item = item.strip("#")
            item = item.upper()
            if len(item) == 0:
                continue
            else:
                try:
                    standardized_list.append(nested_reference_dictionary[key][item])
                except:
                    standardized_list.append(item)

        std_ordered_dict[key] = standardized_list

    return std_ordered_dict




testdict = OrderedDict([('UNIT_TYPE', ['Bldg', 'Apt']),
('UNIT_NUMBER', ['1', '1']),
('STREET_NUMBER', ['1']),
('PRE_DIRECTION', ['e']),
('STREET_NAME', ['Main', 'Test,', 'Test2-', '#Test3']),
('STREET_TYPE', ['Street', ',Test1', '-Test2', 'Test3#']),
('POST_DIRECTION', ['-']),
('UNKNOWN', ['  '])])

print (testdict)
print (standardizer(testdict))