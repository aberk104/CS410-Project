#### CS 410 Project
#### Address Parsing and Matching
#### Alan Berk & Colin Fraser

import pandas as pd
import urllib
from address_compare import parsers as pars
from address_compare import comparers as comp

#file for training/testing
file_name = "small subset Washington State Addresses.xlsx"
address_training_data = pd.read_excel(file_name, dtype= str )
address_training_data['Record_ID'] = address_training_data.index

#split training file into raw data and parsed data
raw_address_training_data = address_training_data[['Record_ID','Single String Address']].copy()
parsed_address_training_data = address_training_data[['Record_ID', 'NUMBER', 'Pre Street Direction', 'Street Name', 'Street Type', 'Post Street Direction', 'CITY', 'STATE', 'POSTCODE']].copy()

#US State Names and Abbreviations from the Open Addresses project on Github
file_path, headers = urllib.request.urlretrieve("https://raw.githubusercontent.com/openaddresses/openaddresses/master/us-data/codes.txt")
us_states = pd.read_csv(file_path, sep='\t')

#US Street Type Abbreviations and Full Names from the Open Addresses project on Github
file_path, headers = urllib.request.urlretrieve("https://raw.githubusercontent.com/openaddresses/expand/master/maps/us")
us_streets = pd.read_csv(file_path, header=None)
us_streets.columns = ['st_abbrev', 'street_type']

#Set of Compass Points for Address Street Names
compass_points_set = {'N','S','E','W','NE','NW','SE','SW','NORTH','SOUTH','EAST','WEST'} #Do we want to include North, South, East, and West as compass points or are they really part of the Street Names themselves?

#Parse Raw Training Data using Naive Parser
for row in range(max(raw_address_training_data.index)):
    for item in pars.naive_parse(raw_address_training_data.loc[row, 'Single String Address']):
        '''
        need to tag each item returned from the naive parse keyed by the Record ID
        i.e., create multi-column table by Record ID and populating the number, street name, etc.
        then compare the parsed output against the parsed_address_training_data
        '''
        pass

print (comp.naive_compare("123 Main","Main 123"))