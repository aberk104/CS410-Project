from address_compare import aggregate_functions as aggf
from address_compare import address_randomizer as add_rndm
import pandas as pd

run_mode = 'comparer_truths' #choose from ['tagger','comparer','comparer_truths','all']


standardize_addresses = True #if True, the tagged address components will be standardized (changed to upper case, unit types, street types, etc. changed to long form names)

use_raw_address_files = True #if False, only the specified number of randomly created addresses above will be used; False only works with the 'comparer' run_mode
num_rndm_addresses_to_create = 1000 #if use_raw_address_files = False, the number of addresses that will be randomly created for use in the tagger and compare functions

field_name_raw_addresses = 'Single String Address' #represents the name of the field in the raw address files containing the raw address (street information)
field_name_record_id = 'Record_ID' #represents the name of the field containing the Record ID in the raw files; if not present in the raw files, populate with None

#file_location_raw_addresses_1 = 'data\\stnd tagged WA addresses - hwy as st type.xlsx'
#file_location_raw_addresses_1 = 'data\\tagged stnd CO Stores - hwy as street type.xlsx'
file_location_raw_addresses_1 = 'data\\MarijuanaApplicants - test data list 1.xlsx'
file_location_raw_addresses_2 = 'data\\MarijuanaApplicants - test data list 2.xlsx'

file_name_ground_truth_matches = 'data\\marijuana applicants test data - correct matches.xlsx'

write_output_to_excel = True #if True, the output from the applicable modes will be written to Excel; otherwise, results will be printed in the notebook

match_5_digit_zip = True #if True, the matchers will only look at the 5 digit zips; if False, the matchers will look at all provided digits

matchtype = 'probabilistic_match' #choose from ['exact_match','probabilistic_match']
prob_threshold = 0.95 #choose a value between 0 and 1, inclusive

compared_dict, matcher_truths_dict = aggf.tag_and_compare_addresses(file_location_raw_addresses_1, file_location_raw_addresses_2, file_name_ground_truth_matches, field_name_record_id, field_name_raw_addresses, standardize_addresses, run_mode, matchtype=matchtype, threshold=prob_threshold, match5zip=match_5_digit_zip)

output_name = 'output\\raw_to_matched_addresses.xlsx'
tagger_writer = pd.ExcelWriter(output_name, engine='xlsxwriter')
for sheet, frame in compared_dict.items():
    frame.to_excel(tagger_writer, sheet_name=sheet)
tagger_writer.save()