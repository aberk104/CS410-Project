'''
The standardizers.py file contains functions to help standardize tagged strings of addresses
'''

from collections import OrderedDict
from collections import defaultdict
import pandas as pd
from address_compare import reference_data as refdt

# Initialize the variables containing the reference data for future use
street_types = refdt.all_us_street_types()
unit_types = refdt.all_us_unit_types()
states = refdt.all_us_states()
compass_points_def, key_val_switch_compass_pts = refdt.compass_points()

# Capitalize the values in the street_types dataframe and convert them into a dictionary
all_caps_street_types_dict = dict()
for row in range(street_types.shape[0]):
    all_caps_street_types_dict[street_types.loc[row, 'st_abbrev'].upper()] = street_types.loc[row, 'street_type'].upper()

# Capitalize the values in the unit_types dataframe and convert them into a dictionary
all_caps_unit_types_dict = dict()
for row in range(unit_types.shape[0]):
    all_caps_unit_types_dict[unit_types.loc[row, 'unit_type_abbrev'].upper()] = unit_types.loc[row, 'unit_type_name'].upper()

# Capitalize the values in the states dataframe and convert them into a dictionary
all_caps_states_dict = dict()
for row in range(states.shape[0]):
    all_caps_states_dict[states.loc[row, 'Postal Code'].upper()] = states.loc[row, 'State'].upper()
    if states.notnull().loc[row, 'Abbreviation']:
        all_caps_states_dict[states.loc[row, 'Abbreviation'].upper()] = states.loc[row, 'State'].upper()

# The following creates a nested dictionary where the first keys are the tags in the ordered dictionary.  These keys represent the keys for the tagged addresses that can be standardized via reference data
nested_ref_dt_dict = defaultdict(dict)
nested_ref_dt_dict['UNIT_TYPE'] = all_caps_unit_types_dict
nested_ref_dt_dict['STREET_TYPE'] = all_caps_street_types_dict
nested_ref_dt_dict['PRE_DIRECTION'] = key_val_switch_compass_pts
nested_ref_dt_dict['POST_DIRECTION'] = key_val_switch_compass_pts
nested_ref_dt_dict['STATE'] = all_caps_states_dict


# The below function will convert the a list of ordered dictionaries into a pandas dataframe, remove duplicates, and repopulate the ordered dictionary
def de_duper(list_ordered_dict, sorter = True):
    addresses = pd.DataFrame(list_ordered_dict)
    for row in range(addresses.shape[0]):
        for col in list(addresses):
            addresses.loc[row, col] = tuple(addresses.loc[row, col])
    addresses = addresses.drop_duplicates()

    if sorter:
        addresses = addresses.sort_values(by=['STATE','CITY','STREET_NAME'])

    addresses = addresses.reset_index(drop=True)

    new_list_ordered_dict = list(OrderedDict())
    for row in range(addresses.shape[0]):
        row_ordered_dict = OrderedDict()
        for col in list(addresses):
            col_list = list(addresses.loc[row,col])
            row_ordered_dict[col] = col_list

        new_list_ordered_dict.append(row_ordered_dict)

    return new_list_ordered_dict


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




# testdict = OrderedDict([('UNIT_TYPE', ['Bldg', 'Apt']),
# ('UNIT_NUMBER', ['1', '1']),
# ('STREET_NUMBER', ['1']),
# ('PRE_DIRECTION', ['e']),
# ('STREET_NAME', ['Main', 'Test,', 'Test2-', '#Test3']),
# ('STREET_TYPE', ['Street', ',Test1', '-Test2', 'Test3#']),
# ('POST_DIRECTION', ['-']),
# ('UNKNOWN', ['  ']),
# ('CITY', ['SEATTLE']),
# ('STATE', ['WA']),
# ('ZIP_CODE', [])])
#
# testdict2 = OrderedDict([('UNIT_TYPE', ['Ste']),
# ('UNIT_NUMBER', ['4']),
# ('STREET_NUMBER', ['5']),
# ('PRE_DIRECTION', []),
# ('STREET_NAME', ['Elm']),
# ('STREET_TYPE', ['Avenue']),
# ('POST_DIRECTION', []),
# ('UNKNOWN', []),
# ('CITY', ['OLYMPIA']),
# ('STATE', ['WA']),
# ('ZIP_CODE', [])])
#
#
# testdict = (standardizer(testdict))
# testdict2 = (standardizer(testdict2))
#
# list_dict = list()
# list_dict.append(testdict)
# list_dict.append(testdict2)
# list_dict_copy = list_dict.copy()
#
# list_dict = (de_duper(list_dict))
#
#
# print (list_dict_copy == list_dict)
#
# print (list_dict)