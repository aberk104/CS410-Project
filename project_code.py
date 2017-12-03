#### CS 410 Project
#### Address Parsing and Matching
#### Alan Berk & Colin Fraser

import pandas as pd
import urllib
from address_compare import parsers as pars
import collections

# sys.path.append("address_compare")
# from address_compare import comparers as comp

# file for training/testing
def training_file(filename, filetype, unstruct_fields, city_state_fields, parsed_fields):
    if filetype == "csv":
        address_training_data = pd.read_csv(filename, dtype= str)
    else:
        address_training_data = pd.read_excel(filename, dtype= str)

    address_training_data['Record_ID'] = address_training_data.index

    unstruct_fields_list = ['Record_ID', unstruct_fields]
    unstruct_fields_list.extend(city_state_fields)
    parsed_fields.insert(0,'Record_ID')
    parsed_fields.extend(city_state_fields)

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

# US Zip Codes with Acceptable City Names and States
def all_us_cities_zips():
    all_fields_us_cities_zips = pd.read_excel("data\zip_code_database.xlsx", dtype=str)
    all_fields_us_cities_zips['zip'] = all_fields_us_cities_zips['zip'].str.zfill(5)

    us_cities_zips = all_fields_us_cities_zips[['zip','primary_city','acceptable_cities','unacceptable_cities','state']].copy()

    return us_cities_zips

# Set of Compass Points for Address Street Names
def compass_points(include_full_names: bool = True):
    if include_full_names:
        compass_points_dict = {'NORTH': {'N','NORTH','N.'}, 'SOUTH': {'S','SOUTH','S.'}, 'EAST': {'E','EAST','E.'}, 'WEST': {'W','WEST','W.'},
                               'NE': {'NE','NE.','N.E.','NORTHEAST'},'NW': {'NW','NW.','N.W.','NORTHWEST'}, 'SE': {'SE','SE.','S.E.','SOUTHEAST'}, 'SW': {'SW','SW.','S.W.','SOUTHWEST'}}
    else:
        compass_points_dict = {'NORTH': {'N','N.'}, 'SOUTH': {'S','S.'}, 'EAST': {'E','E.'}, 'WEST': {'W','W.'},
                               'NE': {'NE','NE.','N.E.'},'NW': {'NW','NW.','N.W.'}, 'SE': {'SE','SE.','S.E.'}, 'SW': {'SW','SW.','S.W.'}}
    return compass_points_dict

# Parse Raw Training Data using Unigram Like Parser and the Naive Parser in the parsers file
def unigram_like_parser(raw_addresses, unstruct_field_name, us_states, us_street_types, us_cities_zips):
    parsed_data_columns = ['Record_ID','Street Number','Unit Type','Unit Number','Pre Street Direction','Street Name','Street Type','Post Street Direction']
    parsed_address_data = pd.DataFrame(index=range(max(raw_addresses.index)),columns=parsed_data_columns)
    us_state_post_codes = list(us_states['Postal Code'])

    city_state_combos_dict = collections.defaultdict(set)
    for row in range(max(us_cities_zips.index)):
        cities = list()

        primary_city = us_cities_zips.loc[row, 'primary_city'].split(',')
        cities.extend(primary_city)

        acceptable_cities = us_cities_zips.loc[row, 'acceptable_cities'].split(',')
        cities.extend(acceptable_cities)

        unacceptable_cities = us_cities_zips.loc[row, 'unacceptable_cities'].split(',')
        cities.extend(unacceptable_cities)

        for city in cities:
            city = city.strip()
            if not city == 'nan':
                city_state_combos_dict[us_cities_zips.loc[row, 'state']].add(city)

    for row in range(max(raw_addresses.index)):
        record_id = raw_addresses.loc[row, 'Record_ID']
        parsed_address_data.loc[row,'Record_ID'] = record_id
        parsed_data = list(pars.naive_parse(raw_addresses.loc[row, unstruct_field_name]))

        parsed_data_copy = parsed_data.copy()

        # for item in parsed_data:
        #     no_comma_item = item.strip(',')
        #     titlecase_item = no_comma_item.title()
        #     if (len(no_comma_item) == 5 and no_comma_item.isdigit()) or (len(no_comma_item) == 10 and no_comma_item[:4].isdigit() and no_comma_item[6:].isdigit() and no_comma_item[5] == "-"):
        #         parsed_address_data.loc[record_id, 'Zip'] = no_comma_item
        #         parsed_data_copy.remove(item)
        #     elif no_comma_item in us_state_post_codes:
        #         parsed_address_data.loc[record_id, 'State'] = no_comma_item
        #         parsed_data_copy.remove(item)
        #     elif titlecase_item in city_state_combos_dict[parsed_address_data.loc[record_id, 'State']]:
        #         parsed_address_data.loc[record_id, 'City'] = no_comma_item
        #         parsed_data_copy.remove(item)



#        if row == 5:
#            break
#        if row < 10:
#            print (parsed_data, parsed_address_data)
#        else:
#            break
#        '''
#        need to tag each item returned from the naive parse keyed by the Record ID
#        i.e., create multi-column table by Record ID and populating the number, street name, etc.
#        then compare the parsed output against the parsed_address_training_data
#        '''

