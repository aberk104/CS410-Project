'''
The standardizers.py file contains functions to help standardize tagged strings of addresses
'''

from collections import OrderedDict
#from collections import defaultdict
import pandas as pd
#from address_compare import reference_data as refdt
import json
import pkg_resources

NESTED_REF_DT_DICT_PATH = pkg_resources.resource_filename('address_compare', 'data/ref_dt_dict.json')


# Import nested dictionary from neste_ref_dt_dict json file
with open(NESTED_REF_DT_DICT_PATH) as json_file:
    nested_ref_dt_dict = json.load(json_file)


# The below function will convert the a list of ordered dictionaries into a pandas dataframe, remove duplicates, and repopulate the ordered dictionary
def de_dupe_sorter(list_ordered_dict, sorter = True):
    '''
    This function converts a list of dictionaries to a pandas dataframe in order to de-duplicate the list.  It is intended to be run after the standardizer function.
    There is an optional sorter as well to allow the user to determine whether or not the records should also be sorted in the dataframe.
    :param list_ordered_dict: This is a list of ordered_dictionaries containing the tagged and standardized address data
    :param sorter: an optional True/False parameter defaulted to True.  If True, the records will be sorted while in the dataframe
    :return: new_list_ordered_dict = the resultant list of ordered dictionaries after de-duping and sorting
    '''
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




def consolidate_address_list(address_df, column_names = None):
    if column_names == None:
        column_names = ['UNIT_TYPE','UNIT_NUMBER','STREET_NUMBER','PRE_DIRECTION','STREET_NAME','STREET_TYPE','POST_DIRECTION','UNKNOWN','CITY','STATE','ZIP_CODE']
    grouped_df = address_df.groupby(column_names, as_index=False)['Record_ID'].apply(list).to_frame().reset_index()
    grouped_df = grouped_df.rename(columns={0:'Record_ID'})
    return grouped_df



def record_id_addition(address_df):
    if 'Record_ID' not in list(address_df):
        address_df['Record_ID'] = address_df.index
    return address_df


def empty_column_addition(address_df, column_names):
    existing_column_names = list(address_df)
    for col in column_names:
        if col not in existing_column_names:
            address_df[col] = ""
    return address_df

#
# test_data = pd.read_excel('data\\sandbox data.xlsx')
# test_data = record_id_addition(test_data)
# column_names = ['UNIT_TYPE','UNIT_NUMBER','STREET_NUMBER','PRE_DIRECTION','STREET_NAME','STREET_TYPE','POST_DIRECTION','UNKNOWN','CITY','STATE','ZIP_CODE']
# test_data = empty_column_addition(test_data, column_names)
# print (test_data)
# column_names = ['Single String Address','UNIT_TYPE','UNIT_NUMBER','STREET_NUMBER','PRE_DIRECTION','STREET_NAME','STREET_TYPE','POST_DIRECTION','UNKNOWN','CITY','STATE','ZIP_CODE']
# grouped = consolidate_address_list(test_data, column_names)
# print (grouped)
# print (list(grouped))
#


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
# list_dict = (de_dupe_sorter(list_dict))
#
#
# print (list_dict_copy == list_dict)
#
# print (list_dict)