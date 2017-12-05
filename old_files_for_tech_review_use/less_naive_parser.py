import pandas as pd
from . import constants as const

def all_us_street_types():
    us_streets = pd.read_csv("data\\us_street_types.csv")
    return us_streets

def compass_points():
    compass_points_dict = const.COMPASS_POINTS_DICT
    switched_key_val_compass_points = dict()
    for key, valset in compass_points_dict.items():
        for val in valset:
            switched_key_val_compass_points[val] = key

    return compass_points_dict, switched_key_val_compass_points

def all_us_unit_types():
    us_unit_types = pd.read_csv("data\\us_unit_types.csv")
    return us_unit_types

def split_training_file(trainingdata, unstruct_fields, parsed_fields):
    raw_address_training_data = trainingdata[unstruct_fields].copy()
    parsed_address_training_data = trainingdata[parsed_fields].copy()
    return raw_address_training_data, parsed_address_training_data

us_streets = all_us_street_types()
#us_states = prjc.all_us_states()
compass_points_def, key_val_switch_compass_pts = compass_points()
#us_cities_zips = prjc.all_us_cities_zips()
us_unit_types = all_us_unit_types()

def test_tagger_parser():
    testing_data = pd.read_excel("data\\tagged washington state address training data.xlsx", dtype=str)
    testing_data['Record_ID'] = testing_data.index
    raw_testing_data, parsed_testing_data = split_training_file(testing_data, ['Record_ID','Single String Address'], ['Record_ID','Tagged Pre Street Direction','Tagged Street Name','Tagged Street Type','Tagged Post Street Direction','Tagged Street Number','Tagged Unit Type','Tagged Unit Number'])

    all_tagger_results = list()
#    for row in range(testing_data.shape[0]):
    for row in range(5):
        raw_address_string = raw_testing_data.loc[row,'Single String Address']
        tagged_street_num = parsed_testing_data.loc[row,'Tagged Street Number'].upper()
        tagged_unit_type = parsed_testing_data.loc[row,'Tagged Unit Type'].upper()
        tagged_unit_num = parsed_testing_data.loc[row, 'Tagged Unit Number'].upper()
        tagged_pre_direct = parsed_testing_data.loc[row, 'Tagged Pre Street Direction'].upper()
        tagged_street_name = parsed_testing_data.loc[row, 'Tagged Street Name'].upper()
        tagged_street_type = parsed_testing_data.loc[row, 'Tagged Street Type'].upper()
        tagged_post_direct = parsed_testing_data.loc[row, 'Tagged Post Street Direction'].upper()

        fixed_address, tagger_result = less_naive_parser_fnc(raw_address_string, us_streets, compass_points_def, key_val_switch_compass_pts, us_unit_types, tagged_street_num, tagged_unit_type, tagged_unit_num,
                                                             tagged_pre_direct, tagged_street_name, tagged_street_type, tagged_post_direct)
        all_tagger_results.append(tagger_result)
        #print (parsed_testing_data.ix[row])
    return all_tagger_results






def less_naive_parser_fnc(address_string: str, street_types = us_streets, compass_points = compass_points_def, switched_compass_points = key_val_switch_compass_pts, unit_types = us_unit_types,
                          tag_st_num = None, tag_unit_type = None, tag_unit_num = None, tag_pre_direct = None, tag_st_name = None, tag_st_type = None, tag_post_direct = None):
    all_caps_addresses = address_string.upper()

    # all_caps_street_types = pd.DataFrame(columns=['st_abbrev','street_type'])
    # all_caps_street_types['st_abbrev'] = street_types['st_abbrev'].str.upper()
    # all_caps_street_types['street_type'] = street_types['street_type'].str.upper()

    split_address_copy = list(all_caps_addresses.split())
    split_address = list()
    for item in split_address_copy:
        if item[len(item)-1] in [",","-"] and len(item) > 1:
            if len(item) == 2:
                split_address.append(item[0])
                split_address.append(item[1])
            else:
                split_address.append(item[:len(item)-1])
                split_address.append(item[len(item)-1])
        elif len(item) > 0:
            split_address.append(item)

    reversed_address_list = split_address.copy()

    if len(reversed_address_list) > 1:
        reversed_address_list.reverse()

    parsed_address_columns = ['street_number','pre_street_direction','street_name','street_type','post_street_direction','unit_type','unit_number', 'unit_type2','unit_number2']

    parsed_address_string = pd.DataFrame(columns=parsed_address_columns, dtype=str)

    all_caps_street_types_dict = dict()
    for row in range(street_types.shape[0]):
        all_caps_street_types_dict[street_types.loc[row, 'st_abbrev'].upper()] = street_types.loc[row, 'street_type'].upper()


    all_caps_unit_types_dict = dict()
    for row in range(unit_types.shape[0]):
        all_caps_unit_types_dict[unit_types.loc[row, 'unit_type_abbrev'].upper()] = unit_types.loc[row, 'unit_type_name'].upper()

    total_items_address_list = len(split_address) - 1

    item_index_number = 0
    item_index_number_to_remove = 0
    street_type_index = None
    post_street_direction_index = None
    pre_street_direction_index = None
    unit_type_index = None
    unit_type_index2 = None
    reversed_address_list_copy = reversed_address_list.copy()
    for item in reversed_address_list:
        if item in all_caps_street_types_dict.keys() and street_type_index == None:
            parsed_address_string.loc[0,'street_type'] = all_caps_street_types_dict[item]
            street_type_index = total_items_address_list - item_index_number
            reversed_address_list_copy.pop(item_index_number_to_remove)
            item_index_number_to_remove -= 1
        elif item in all_caps_street_types_dict.values() and street_type_index == None:
            parsed_address_string.loc[0,'street_type'] = item
            street_type_index = total_items_address_list - item_index_number
            reversed_address_list_copy.pop(item_index_number_to_remove)
            item_index_number_to_remove -= 1
        elif item in switched_compass_points.keys() and (post_street_direction_index == None or pre_street_direction_index == None):
            if street_type_index == None:
                parsed_address_string.loc[0,'post_street_direction'] = switched_compass_points[item]
                post_street_direction_index = total_items_address_list - item_index_number
                reversed_address_list_copy.pop(item_index_number_to_remove)
                item_index_number_to_remove -= 1
            else:
                parsed_address_string.loc[0,'pre_street_direction'] = switched_compass_points[item]
                pre_street_direction_index = total_items_address_list - item_index_number
                reversed_address_list_copy.pop(item_index_number_to_remove)
                item_index_number_to_remove -= 1
        elif item in all_caps_unit_types_dict.keys() and (unit_type_index == None or unit_type_index2 == None):
            if unit_type_index == None:
                parsed_address_string.loc[0,'unit_type'] = all_caps_unit_types_dict[item]
                unit_type_index = total_items_address_list - item_index_number
                reversed_address_list_copy.pop(item_index_number_to_remove)
                item_index_number_to_remove -= 1
            else:
                parsed_address_string.loc[0,'unit_type2'] = all_caps_unit_types_dict[item]
                unit_type_index2 = total_items_address_list - item_index_number
                reversed_address_list_copy.pop(item_index_number_to_remove)
                item_index_number_to_remove -= 1
        elif item in all_caps_unit_types_dict.values() and (unit_type_index == None or unit_type_index2 == None):
            if unit_type_index == None:
                parsed_address_string.loc[0,'unit_type'] = item
                unit_type_index = total_items_address_list - item_index_number
                reversed_address_list_copy.pop(item_index_number_to_remove)
                item_index_number_to_remove -= 1
            else:
                parsed_address_string.loc[0,'unit_type2'] = item
                unit_type_index2 = total_items_address_list - item_index_number
                reversed_address_list_copy.pop(item_index_number_to_remove)
                item_index_number_to_remove -= 1

        item_index_number += 1
        item_index_number_to_remove += 1


#### need to figure out a better way to remove a word so that it doesn't cause a failure.  3615 E Front St causes an error as Front is a Unit type and removed from the reversed list which causes a failure since it's also between E and ST which tries to read it as the street name
    concat_street_name = str()
    if pre_street_direction_index != None and street_type_index != None:
        num_items_for_name = street_type_index - pre_street_direction_index - 1
        for num in range(num_items_for_name):
            concat_street_name += split_address[pre_street_direction_index + num + 1] + " "
            if split_address[pre_street_direction_index + num + 1] in reversed_address_list_copy:
                reversed_address_list_copy.remove(split_address[pre_street_direction_index + num + 1])
        concat_street_name = concat_street_name.strip()
    else:
        '''
        Need to add ELIFs for when the pre_street_direction_index is None.
        I.e., in that situation what is the starting point for the street name and what is the ending point
        Also need to consider what to do when street_type_index is None as there is at least 1 Washington Address called Broadway without a street type
        '''
        pass

    concat_unit_number = str()
    if unit_type_index != None:
        if pre_street_direction_index != None and (pre_street_direction_index - unit_type_index) > 1:
            num_items_for_unit = pre_street_direction_index - unit_type_index - 1
            for num in range(num_items_for_unit):
                if split_address[unit_type_index + num + 1] in [",","-"]:
                    break
                else:
                    concat_unit_number += split_address[unit_type_index + num + 1] + " "
                    reversed_address_list_copy.remove(split_address[unit_type_index + num + 1])
            concat_unit_number = concat_unit_number.strip()

        elif post_street_direction_index != None and (unit_type_index > post_street_direction_index):
            num_items_for_unit = total_items_address_list - unit_type_index
            for item in split_address[unit_type_index+1:]:
                concat_unit_number += item + " "
                reversed_address_list_copy.remove(item)
            concat_unit_number = concat_unit_number.strip()

            '''
            Need to add ELIFs for when the pre_street_direction_index is None.
            I.e., in that situation, what is the ending point for the unit number (how to determine the starting point of the thing after the unit number
            Also need to consider the situation where the unit number is before the unit type.  Need to determine how many items prior to the unit type would make up the unit number in this case
            Also need to consider the situation where the unit type and number come at the end of the street
            So need separate If and Elses for pre_street_direction_index != None for when the difference is 1 and for when the difference is negative
            '''

            pass

    remaining_items_in_list = reversed_address_list_copy.copy()
    if len(remaining_items_in_list) > 1:
        remaining_items_in_list.reverse()
    concat_street_number = str()
    if len(remaining_items_in_list) > 0:
        for item in remaining_items_in_list:
            concat_street_number += item + " "
    concat_street_number = concat_street_number.strip()

    parsed_address_string.loc[0, 'street_name'] = concat_street_name
    parsed_address_string.loc[0, 'unit_number'] = concat_unit_number
    parsed_address_string.loc[0, 'street_number'] = concat_street_number

    reconcatenated_address = str()
    for column in parsed_address_columns:
        if parsed_address_string.notnull().loc[0, column]:
            reconcatenated_address += str(parsed_address_string.loc[0, column]) + " "
    reconcatenated_address = reconcatenated_address.strip()

    correctly_parsed_address_result = None
    if not tag_st_name == None:
        test_street_num = parsed_address_string.loc[0,'street_number']
        test_unit_type = parsed_address_string.loc[0,'unit_type']
        test_unit_num = parsed_address_string.loc[0, 'unit_number']
        test_pre_direct = parsed_address_string.loc[0, 'pre_street_direction']
        test_street_name = parsed_address_string.loc[0, 'street_name']
        test_street_type = parsed_address_string.loc[0, 'street_type']
        test_post_direct = parsed_address_string.loc[0, 'post_street_direction']
        if not tag_st_type == "NAN":
            try:
                tag_st_type = all_caps_street_types_dict[tag_st_type]
            except:
                tag_st_type = tag_st_type
        if not tag_unit_type == "NAN":
            try:
                tag_unit_type = all_caps_unit_types_dict[tag_unit_type]
            except:
                tag_unit_type = tag_unit_type
        correctly_parsed_address_result = parsed_address_compare(test_street_num, test_pre_direct, test_street_name, test_street_type, test_post_direct, test_unit_type, test_unit_num, tag_st_num, tag_pre_direct,
                                                                 tag_st_name, tag_st_type, tag_post_direct, tag_unit_type, tag_unit_num)
    #print (parsed_address_string)
    return reconcatenated_address, correctly_parsed_address_result

def parsed_address_compare(test_st_num, test_pre_direct, test_st_name, test_st_type, test_post_direct, test_unit_type, test_unit_num,
                           tagged_st_num, tagged_pre_direct, tagged_st_name, tagged_st_type, tagged_post_direct, tagged_unit_type, tagged_unit_num):

    # print("start")
    # print (test_st_num, tagged_st_num, test_st_num == tagged_st_num)
    # print (test_pre_direct, tagged_pre_direct, test_pre_direct == tagged_pre_direct)
    # print (test_st_name, tagged_st_name, test_st_name == tagged_st_name)
    # print (test_st_type, tagged_st_type, test_st_type == tagged_st_type)
    # print (test_post_direct, tagged_post_direct, test_post_direct == tagged_post_direct)
    # print (test_unit_type, tagged_unit_type, test_unit_type == tagged_unit_type)
    # print (test_unit_num, tagged_unit_num, test_unit_num == tagged_unit_num)
    # print ("")

    if ((test_st_num == tagged_st_num) or (str(test_st_num) in ['Nan','NAN','nan', None] and str(tagged_st_num) in ['Nan','NAN','nan'])) and \
            ((test_pre_direct == tagged_pre_direct) or (str(test_pre_direct) in ['Nan','NAN','nan', None] and str(tagged_pre_direct) in ['Nan','NAN','nan'])) and \
            ((test_st_name == tagged_st_name) or (str(test_st_name) in ['Nan','NAN','nan', None] and str(tagged_st_name) in ['Nan','NAN','nan'])) and \
            ((test_st_type == tagged_st_type) or (str(test_st_type) in ['Nan','NAN','nan', None] and str(tagged_st_type) in ['Nan','NAN','nan'])) and \
            ((test_post_direct == tagged_post_direct) or (str(test_post_direct) in ['Nan','NAN','nan', None] and str(tagged_post_direct) in ['Nan','NAN','nan'])) and \
            ((test_unit_type == tagged_unit_type) or (str(test_unit_type) in ['Nan','NAN','nan', None] and str(tagged_unit_type) in ['Nan','NAN','nan'])) and \
            ((test_unit_num == tagged_unit_num) or (str(test_unit_num) in ['Nan','NAN','nan', None] and str(tagged_unit_num) in ['Nan','NAN','nan'])):
        return True
    else:
        return False
