#### CS 410 Project
#### Address Parsing and Matching
#### Alan Berk & Colin Fraser

import pandas as pd
import urllib


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


