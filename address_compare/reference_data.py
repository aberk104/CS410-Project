'''
The reference_data.py file contains functions that create reference tables of US Street Types, US States, US Unit Types, and US City/State/Zip combinations.
These tables will be used in the standardizers.py file to standardize the ordered dictionaries containing the addresses.
This file only needs to be called/run if changes are made to the source data.  Otherwise, all output is written to json files stored in the data folders
'''

import pandas as pd
from address_compare import constants as const
from collections import defaultdict
import json

def all_us_states():
    '''
    The all_us_states function has no inputs.  It creates a table of US State Names and Abbreviations originally sourced from the Open Addresses project on Github
    :return: us_states
    '''
    us_states = pd.read_csv("data\\us_states.csv")
    return us_states


def all_us_street_types():
    '''
    The all_us_street_types function has no inputs.  It creates a table of US Street Type Abbreviations and Full Names originally sourced from the Open Addresses project on Github
    :return: us_streets
    '''
    us_streets = pd.read_csv("data\\us_street_types.csv")
    return us_streets


def all_us_unit_types():
    '''
    The all_us_unit_types function has no inputs. It creates a table of US Unit Types and Abbreviations originally Sourced from the USPS
    :return: us_unit_types
    '''
    us_unit_types = pd.read_csv("data\\us_unit_types.csv")
    return us_unit_types


def all_us_cities_zips():
    '''
    The all_us_cities_zips function has no inputs. It creates a table of US Cities with the corresponding zip code and state originally sourced from https://www.unitedstateszipcodes.org/zip-code-database/
    :return: us_cities_zips
    '''
    all_fields_us_cities_zips = pd.read_excel("data\\zip_code_database.xlsx", dtype=str)
    all_fields_us_cities_zips['zip'] = all_fields_us_cities_zips['zip'].str.zfill(5)

    us_cities_zips = all_fields_us_cities_zips[['zip','primary_city','acceptable_cities','unacceptable_cities','state']].copy()
    return us_cities_zips


def compass_points():
    '''
    The compass_points function has no inputs.  It creates 2 dictionaries of compass points with their abbreviated and long forms from the constants.py file
    :return: compass_points_dict (keys are the long form version of each compass point), switched_key_val_compass_points (keys are the abbreviated version of each compass point
    '''
    compass_points_dict = const.COMPASS_POINTS_DICT
    switched_key_val_compass_points = dict()
    for key, valset in compass_points_dict.items():
        for val in valset:
            switched_key_val_compass_points[val] = key

    return compass_points_dict, switched_key_val_compass_points



# Initialize the variables containing the reference data for future use
street_types = all_us_street_types()
unit_types = all_us_unit_types()
states = all_us_states()
compass_points_def, key_val_switch_compass_pts = compass_points()
city_zip_state = all_us_cities_zips()

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

# Capitalize values in the city/state/zip dataframe and convert them into a dictionary
state_to_zip_dict = defaultdict(list)
zip_to_primary_city = dict()
for row in range(city_zip_state.shape[0]):
    state_to_zip_dict[city_zip_state.loc[row, 'state'].upper()].append(city_zip_state.loc[row, 'zip'])
    zip_to_primary_city[city_zip_state.loc[row, 'zip']] = city_zip_state.loc[row,'primary_city'].upper()


# The following creates a nested dictionary where the first keys are the tags in the ordered dictionary.  These keys represent the keys for the tagged addresses that can be standardized via reference data
nested_ref_dt_dict = defaultdict(dict)
nested_ref_dt_dict['UNIT_TYPE'] = all_caps_unit_types_dict
nested_ref_dt_dict['STREET_TYPE'] = all_caps_street_types_dict
nested_ref_dt_dict['PRE_DIRECTION'] = key_val_switch_compass_pts
nested_ref_dt_dict['POST_DIRECTION'] = key_val_switch_compass_pts
nested_ref_dt_dict['STATE'] = all_caps_states_dict

with open('data\\ref_dt_dict.json', 'w') as outfile:
    json.dump(nested_ref_dt_dict, outfile)

with open('data\\state_zip_dict.json', 'w') as outfile:
    json.dump(state_to_zip_dict, outfile)

with open('data\\zip_prim_city.json', 'w') as outfile:
    json.dump(zip_to_primary_city, outfile)