'''
The reference_data.py file contains functions that create reference tables of US Street Types, US States, US Unit Types, and US City/State/Zip combinations.
These tables will be used in the standardizers.py file to standardize the ordered dictionaries containing the addresses
'''

import pandas as pd
from address_compare import constants as const

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

