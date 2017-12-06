'''
The master_control_file is the main file.  It calls the functions from all other files and contains the non-functionalized code
'''


from collections import defaultdict
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