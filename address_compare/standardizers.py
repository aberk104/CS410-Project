'''
The standardizers.py file contains functions to help standardize tagged strings of addresses.  It starts with the previously computed
dictionaries and nested dictionaries from the reference_data.py file and stored as JSON files.  It includes functions to standardize addresses, cities, find errors in zip codes,
and add missing columns to the raw address dataframes.
'''

from collections import OrderedDict
#from collections import defaultdict
import pandas as pd
#from address_compare import reference_data as refdt
import json
import pkg_resources

NESTED_REF_DT_DICT_PATH = pkg_resources.resource_filename('address_compare', 'data/ref_dt_dict.json')
STATE_ZIP_DT_DICT_PATH = pkg_resources.resource_filename('address_compare', 'data/state_zip_dict.json')
ZIP_CITY_DT_DICT_PATH = pkg_resources.resource_filename('address_compare', 'data/zip_prim_city.json')


# Import nested dictionary from neste_ref_dt_dict json file
with open(NESTED_REF_DT_DICT_PATH) as json_file:
    nested_ref_dt_dict = json.load(json_file)

# Import State Zip Dictionary from Json file
with open(STATE_ZIP_DT_DICT_PATH) as json_file:
    state_zip_dict = json.load(json_file)

# Import Zip City Dictionary from Json File:
with open(ZIP_CITY_DT_DICT_PATH) as json_file:
    zip_city_dict = json.load(json_file)



# The below function will convert the a list of ordered dictionaries into a pandas dataframe, remove duplicates, and repopulate the ordered dictionary
# def de_dupe_sorter(list_ordered_dict, sorter = True):
#     '''
#     This function converts a list of dictionaries to a pandas dataframe in order to de-duplicate the list.  It is intended to be run after the standardizer function.
#     There is an optional sorter as well to allow the user to determine whether or not the records should also be sorted in the dataframe.
#     :param list_ordered_dict: This is a list of ordered_dictionaries containing the tagged and standardized address data
#     :param sorter: an optional True/False parameter defaulted to True.  If True, the records will be sorted while in the dataframe
#     :return new_list_ordered_dict: the resultant list of ordered dictionaries after de-duping and sorting
#     '''
#     addresses = pd.DataFrame(list_ordered_dict)
#     for row in range(addresses.shape[0]):
#         for col in list(addresses):
#             addresses.loc[row, col] = tuple(addresses.loc[row, col])
#     addresses = addresses.drop_duplicates()
#
#     if sorter:
#         addresses = addresses.sort_values(by=['STATE','CITY','STREET_NAME'])
#
#     addresses = addresses.reset_index(drop=True)
#
#     new_list_ordered_dict = list(OrderedDict())
#     for row in range(addresses.shape[0]):
#         row_ordered_dict = OrderedDict()
#         for col in list(addresses):
#             col_list = list(addresses.loc[row,col])
#             row_ordered_dict[col] = col_list
#
#         new_list_ordered_dict.append(row_ordered_dict)
#
#     return new_list_ordered_dict


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
    '''
    This function is used to group identical records within an individual dataframe as a way to remove duplicates.
    :param address_df: a dataframe with parsed/tagged addresses that will be grouped (consolidated/de-duped)
    :param column_names: the field names that will be used to group the records in the dataframe.  If None, the default field names from the CRF tagger will be used
    :return grouped_df: a new dataframe where identical recoreds are grouped together (consolidated/de-duped)
    '''
    if column_names == None:
        column_names = ['UNIT_TYPE','UNIT_NUMBER','STREET_NUMBER','PRE_DIRECTION','STREET_NAME','STREET_TYPE','POST_DIRECTION','UNKNOWN','CITY','STATE','ZIP_CODE']
    try:
        grouped_df = address_df.groupby(column_names, as_index=False)['Record_ID'].apply(tuple).to_frame().reset_index()
    except:
        grouped_df = address_df.groupby(column_names, as_index=False)['Record_ID'].apply(tuple).reset_index()
    grouped_df = grouped_df.rename(columns={0:'Record_ID'})
    return grouped_df



def record_id_addition(address_df, field_name_rec_id = None):
    '''
    This function is used to add a new field called Record_ID or rename an existing record ID field to the standardized 'Record_ID'
    :param address_df: The dataframe to which the 'Record_ID needs to be added
    :param field_name_rec_id: the name of the Record_ID field in the dataframe.  If None, there is no record ID in the Dataframe and a new field will be added called Record_ID
    :return address_df: a new dataframe with the addition of the Record_ID field
    '''

    if field_name_rec_id == None:
        address_df['Record_ID'] = address_df.index
    else:
        address_df = address_df.rename(columns={field_name_rec_id:'Record_ID'})
    return address_df


def empty_column_addition(address_df, column_names):
    '''
    This function is used to add missing fields to the dataframe (City, State, Zip_Code, Unknown) that are required for the remainder of the match functions
    :param address_df: The dataframe to which the new columns need to be added
    :param column_names: The new columns that need to be added if they don't already exist in the dataframe
    :return address_df: a new dataframe with the addition of the missing columns (if they don't already exist in the dataframe)
    '''
    existing_column_names = list(address_df)
    for col in column_names:
        if col not in existing_column_names:
            address_df[col] = ""
    return address_df



def fix_cities_zips(address_df, state_to_zip_dict = state_zip_dict, zip_prim_city_dict = zip_city_dict):
    '''
    This function is used to standardize and fix the cities and zip codes.  The 'primary_city' for the zip_code per the USPS will replace the existing value in the City field.
    Zip codes that are not valid for the applicable state will be flagged as errors
    :param address_df: the dataframe containing cities, states, and zip codes
    :param state_to_zip_dict: a dictionary containing all valid 5 digit zip codes for the applicable state
    :param zip_prim_city_dict: a dictionary containing the USPS 'primary_city' for the applicable zip code
    :return new_address_df: a new dataframe flagging zip_codes with errors as well as the standardized cities
    '''


    new_address_df = address_df.copy()
    new_address_df['Zip_Code_Error'] = ""
    for row in range(address_df.shape[0]):
        try:
            zip_code_for_test = str(new_address_df.loc[row, 'ZIP_CODE'])
            zip_code_for_test = zip_code_for_test if len(zip_code_for_test) <= 5 else zip_code_for_test[:5]
            if zip_code_for_test not in state_to_zip_dict[new_address_df.loc[row, 'STATE']]:
                new_address_df.loc[row, 'Zip_Code_Error'] = "Yes"
            else:
                new_address_df.loc[row, 'Zip_Code_Error'] = "No"
                new_address_df.loc[row, 'CITY'] = zip_prim_city_dict[zip_code_for_test]
        except:
            new_address_df.loc[row,'Zip_Code_Error'] = "N/A"

    return new_address_df