#### CS 410 Project
#### Address Parsing and Matching
#### Alan Berk & Colin Fraser

import pandas as pd
import urllib
from address_compare import parsers as pars
# from address_compare import comparers as comp

# file for training/testing
def training_file(filename, filetype, unstruct_fields, parsed_fields):
    if filetype == "csv":
        address_training_data = pd.read_csv(filename, dtype= str)
    else:
        address_training_data = pd.read_excel(filename, dtype= str)

    address_training_data['Record_ID'] = address_training_data.index

    unstruct_fields_list = [unstruct_fields]
    unstruct_fields_list.append('Record_ID')

    unstruct_addresses, parsed_addresses = split_training_file(address_training_data, unstruct_fields_list, parsed_fields)
    return unstruct_addresses, parsed_addresses

# split training file into raw data and parsed data
def split_training_file(trainingdata, unstruct_fields, parsed_fields):
    raw_address_training_data = trainingdata[unstruct_fields].copy()
    parsed_address_training_data = trainingdata[parsed_fields].copy()
    return raw_address_training_data, parsed_address_training_data

# US State Names and Abbreviations from the Open Addresses project on Github
def all_us_states():
    file_path, headers = urllib.request.urlretrieve("https://raw.githubusercontent.com/openaddresses/openaddresses/master/us-data/codes.txt")
    us_states = pd.read_csv(file_path, sep='\t')
    return us_states

# US Street Type Abbreviations and Full Names from the Open Addresses project on Github
def all_us_street_types():
    file_path, headers = urllib.request.urlretrieve("https://raw.githubusercontent.com/openaddresses/expand/master/maps/us")
    us_streets = pd.read_csv(file_path, header=None)
    us_streets.columns = ['st_abbrev', 'street_type']
    return us_streets

# Set of Compass Points for Address Street Names
def compass_points(include_full_names: bool = True):
    if include_full_names:
        compass_points_set = {'N','S','E','W','NE','NW','SE','SW','NORTH','SOUTH','EAST','WEST'}
    else:
        compass_points_set = {'N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'}
    return compass_points_set

# Parse Raw Training Data using Naive Parser
# for row in range(max(raw_address_training_data.index)):
#    for item in pars.naive_parse(raw_address_training_data.loc[row, 'Single String Address']):
#        '''
#        need to tag each item returned from the naive parse keyed by the Record ID
#        i.e., create multi-column table by Record ID and populating the number, street name, etc.
#        then compare the parsed output against the parsed_address_training_data
#        '''
#        pass

#print (comp.naive_compare("123 Main","Main 123"))