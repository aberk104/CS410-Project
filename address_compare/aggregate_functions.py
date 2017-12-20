'''
This file contains aggregated functions to tag and match addresses
'''
import pandas as pd
from address_compare import standardizers as stndrdzr
from address_compare import tagging as crf
from address_compare import matcher as mtch
from address_compare import prob_matchers as prob_mtch
from collections import OrderedDict
import sklearn.metrics


missing_columns_from_file = ['CITY', 'STATE', 'ZIP_CODE', 'UNKNOWN']
ground_truth_columns = ['Record_ID', 'Tagged Street Number', 'Tagged Pre Street Direction', 'Tagged Street Name',
                        'Tagged Street Type', 'Tagged Post Street Direction', 'Tagged Unit Type',
                        'Tagged Unit Number']


def __pvt_tag_vs_ground_truths(tagged_file, testfile, ground_truth_cols = ground_truth_columns):

    # Add Record_ID Field to Tagged Addresses
    crf_tagged_test_file = tagged_file.join(testfile['Record_ID'])

    # Create Dataframe with Ground Truth Columns
    manual_tagged_test_file = testfile[ground_truth_cols].copy()

    # Rename Ground Truth Columns
    manual_tagged_test_file = manual_tagged_test_file.rename(columns={'Tagged Street Number': 'STREET_NUMBER',
                                                                      'Tagged Pre Street Direction': 'PRE_DIRECTION',
                                                                      'Tagged Street Name': 'STREET_NAME',
                                                                      'Tagged Street Type': 'STREET_TYPE',
                                                                      'Tagged Post Street Direction': 'POST_DIRECTION',
                                                                      'Tagged Unit Type': 'UNIT_TYPE',
                                                                      'Tagged Unit Number': 'UNIT_NUMBER'})

    # Match Tagger vs. Ground Truth Columns
    cols_for_matcher = ['UNIT_TYPE', 'UNIT_NUMBER', 'STREET_NUMBER', 'PRE_DIRECTION', 'STREET_NAME', 'STREET_TYPE',
                        'POST_DIRECTION']
    correctly_tagged_addresses = mtch.exact_matcher(crf_tagged_test_file, manual_tagged_test_file, cols_for_matcher)

    # Create New Dataframe with Incorrect Addresses
    incorrectly_tagged_addresses = crf_tagged_test_file.mask(crf_tagged_test_file.Record_ID.isin(correctly_tagged_addresses['Record_ID_list_1'])).dropna()
    incorrectly_tagged_addresses = incorrectly_tagged_addresses.merge(testfile[ground_truth_cols], on='Record_ID')

    # Calculate Tagger Metrics
    total_records = crf_tagged_test_file.shape[0]
    correctly_tagged = correctly_tagged_addresses.shape[0]
    incorrectly_tagged = incorrectly_tagged_addresses.shape[0]

    tagger_accuracy = correctly_tagged / total_records

    metrics_dict = OrderedDict()
    precision_dict = OrderedDict()
    recall_dict = OrderedDict()
    fscore_dict = OrderedDict()
    overallacc_dict = OrderedDict()

    for col in cols_for_matcher:
        precision, recall, fscore, ignore = sklearn.metrics.precision_recall_fscore_support(manual_tagged_test_file[col], crf_tagged_test_file[col], average='micro')
        precision_dict[col] = precision
        recall_dict[col] = recall
        fscore_dict[col] = fscore
        overallacc_dict[col] = None

    precision_dict['overall_accuracy'] = None
    recall_dict['overall_accuracy'] = None
    fscore_dict['overall_accuracy'] = None
    overallacc_dict['overall_accuracy'] = tagger_accuracy

    metrics_dict['precision'] = precision_dict
    metrics_dict['recall'] = recall_dict
    metrics_dict['fscore'] = fscore_dict
    metrics_dict['overall_accuracy'] = overallacc_dict

    metrics_df = pd.DataFrame(metrics_dict)

    # Dictionary of DataFrames for Excel Tagger Test File
    dataframes_for_tagger_excel = {'test_data_file': testfile,
                                   'crf_tagged_output': tagged_file,
                                   'crf_output_w_id': crf_tagged_test_file,
                                   'ground_truth_test_file': manual_tagged_test_file,
                                   'correctly_tagged': correctly_tagged_addresses,
                                   'incorrectly_tagged': incorrectly_tagged_addresses,
                                   'tagger_metrics': metrics_df}

    return dataframes_for_tagger_excel


def __pvt_compare_2_address_lists(rawlist1, rawlist2, taggedlist1, taggedlist2, runmode = 'comparer', to_standardize=True, matchtype = 'exact_match', threshold = 0.95):

    # Standardize/Fix Cities and States.  Add a column to denote records with Zip Code Errors
    if to_standardize:
        rawlist1 = stndrdzr.fix_cities_zips(rawlist1)
        rawlist2 = stndrdzr.fix_cities_zips(rawlist2)
    else:
        rawlist1['Zip_Code_Error'] = 'N/A'
        rawlist2['Zip_Code_Error'] = 'N/A'

    # Add Remaining Columns from Raw Address Dataframes to Tagged Address Dataframes
    joined_address_list_1 = taggedlist1.join(rawlist1[['Record_ID', 'CITY', 'STATE', 'ZIP_CODE', 'UNKNOWN', 'Zip_Code_Error']])
    joined_address_list_2 = taggedlist2.join(rawlist2[['Record_ID', 'CITY', 'STATE', 'ZIP_CODE', 'UNKNOWN', 'Zip_Code_Error']])

    # Remove Addresses with Zip Code Errors (I.e., where the Zip Code is not valid for the given state)
    error_addresses_list_1 = joined_address_list_1.where(joined_address_list_1.Zip_Code_Error == "Yes").dropna()
    error_addresses_list_2 = joined_address_list_2.where(joined_address_list_2.Zip_Code_Error == "Yes").dropna()

    # Only Addresses without Zip Code Errors (I.e., where the Zip Code is valid for the given state)
    nonerror_addresses_list_1 = joined_address_list_1.where(joined_address_list_1.Zip_Code_Error.isin(["No","N/A"])).dropna().reset_index()
    nonerror_addresses_list_2 = joined_address_list_2.where(joined_address_list_2.Zip_Code_Error.isin(["No","N/A"])).dropna().reset_index()

    # Fix the type of the Record_ID and ZIP_CODE columns
    try:
        nonerror_addresses_list_1 = nonerror_addresses_list_1.astype({'Record_ID': 'int', 'ZIP_CODE': 'int'})
        nonerror_addresses_list_2 = nonerror_addresses_list_2.astype({'Record_ID': 'int', 'ZIP_CODE': 'int'})
        nonerror_addresses_list_1 = nonerror_addresses_list_1.astype({'Record_ID': 'str', 'ZIP_CODE': 'str'})
        nonerror_addresses_list_2 = nonerror_addresses_list_2.astype({'Record_ID': 'str', 'ZIP_CODE': 'str'})
    except:
        nonerror_addresses_list_1 = nonerror_addresses_list_1.astype({'Record_ID': 'int'})
        nonerror_addresses_list_2 = nonerror_addresses_list_2.astype({'Record_ID': 'int'})
        nonerror_addresses_list_1 = nonerror_addresses_list_1.astype({'Record_ID': 'str'})
        nonerror_addresses_list_2 = nonerror_addresses_list_2.astype({'Record_ID': 'str'})

    # Intra-Grouping of Tagged Address Lists to Consolidate Duplicates
    if runmode == 'comparer':
        grouped_address_list_1 = stndrdzr.consolidate_address_list(nonerror_addresses_list_1)
        grouped_address_list_2 = stndrdzr.consolidate_address_list(nonerror_addresses_list_2)
    else:
        grouped_address_list_1 = nonerror_addresses_list_1.copy()
        grouped_address_list_2 = nonerror_addresses_list_2.copy()

    # Call Either the Exact Match or Learning Match Functions to match the 2 lists
    if matchtype == 'exact_match':
        matches = mtch.exact_matcher(grouped_address_list_1, grouped_address_list_2)
    else:
        pm = prob_mtch.ProbMatcher()
        matches_all_cols = pm.match_probabilities(grouped_address_list_1, grouped_address_list_2, threshold)
        matches_all_cols = matches_all_cols.merge(grouped_address_list_1,left_on='index_1', right_index=True )
        matches_all_cols = matches_all_cols.rename(columns={'Record_ID':'Record_ID_list_1'})
        matches_all_cols = matches_all_cols.merge(grouped_address_list_2,left_on='index_2', right_index=True )
        matches_all_cols = matches_all_cols.rename(columns={'Record_ID':'Record_ID_list_2'})
#        output_name = 'data\\raw_to_matched_addresses_all_cols_test.xlsx'
#        matches_all_cols.to_excel(output_name)
        matches = matches_all_cols[['Record_ID_list_1','Record_ID_list_2','probs']]

    # Create Separate Dataframe for Unmatched Addresses
    unmatched_address_list_1 = grouped_address_list_1.mask(grouped_address_list_1.Record_ID.isin(matches['Record_ID_list_1'])).dropna()
    unmatched_address_list_2 = grouped_address_list_2.mask(grouped_address_list_2.Record_ID.isin(matches['Record_ID_list_2'])).dropna()

    # Dictionary of DataFrames for Excel File
    dataframes_for_excel = {'raw_addresses_list1': rawlist1,
                            'raw_addresses_list2': rawlist2,
                            'zip_errors_list1': error_addresses_list_1,
                            'zip_errors_list2': error_addresses_list_2,
                            'exact_matches': matches,
                            'unmatched_list_1': unmatched_address_list_1,
                            'unmatched_list_2': unmatched_address_list_2}

    return dataframes_for_excel


def __pvt_address_compare_vs_ground_truths(groundtruths, compeddict, groundtruth_matchtypes=["Exact", "Standardized Exact"]):
    # Create Dataframe for Ground Truths
    manual_matches = pd.read_excel(groundtruths, keep_default_na=False, dtype=str)

    # Split out only the applicable Match Types
    golden_exact_matches = manual_matches.where(manual_matches.Match_Type.isin(groundtruth_matchtypes)).dropna().reset_index()

    # Split out Dataframe for Matched Addresses
    matched_addresses = compeddict['exact_matches']

    # Columns with Matched Record IDs
    join_cols = ['Record_ID_list_1', 'Record_ID_list_2']

    # Split out Columns with the Matched Record IDs from Modeled Results
    subset_columns_exact_matches = matched_addresses[join_cols].copy()
    subset_columns_exact_matches['row_index'] = subset_columns_exact_matches.index

    # Split out Columns with the Matched Record IDs from Ground Truths
    subset_cols_golden_exact_matches = golden_exact_matches[join_cols].copy()
    subset_cols_golden_exact_matches['row_index'] = subset_cols_golden_exact_matches.index

    # Change Dataframe Columns to be Strings
    subset_columns_exact_matches = subset_columns_exact_matches.astype(str)
    subset_cols_golden_exact_matches = subset_cols_golden_exact_matches.astype(str)

    # Compare Model Results vs. Ground Truths
    test_vs_golden_compare = mtch.exact_matcher(subset_columns_exact_matches, subset_cols_golden_exact_matches,
                                                join_cols)

    # Create Dataframe with Ground Truth Matches not in Model Results
    missing_golden_matches = subset_cols_golden_exact_matches.mask(
        subset_cols_golden_exact_matches.row_index.isin(test_vs_golden_compare.row_index_list_2)).dropna()

    # Create Dataframe with Modeled Matches not in Ground Truths
    matches_not_in_golden = subset_columns_exact_matches.mask(
        subset_columns_exact_matches.row_index.isin(test_vs_golden_compare.row_index_list_1)).dropna()

    # Extract Dataframes from Dictionary of the Raw Address Lists
    rawlist1 = compeddict['raw_addresses_list1']
    rawlist2 = compeddict['raw_addresses_list2']

    # Calculate Metrics for Model vs. Ground Truths
    total_records_list_1 = rawlist1.shape[0]
    total_records_list_2 = rawlist2.shape[0]
    total_modeled_matches = matched_addresses.shape[0]
    total_manual_exact_matches = golden_exact_matches.shape[0]
    total_correct_positive_matches = test_vs_golden_compare.shape[0]
    false_negatives = missing_golden_matches.shape[0]
    false_positives = matches_not_in_golden.shape[0]

    accuracy_val_list_1 = total_correct_positive_matches / total_records_list_1
    accuracy_val_list_2 = total_correct_positive_matches / total_records_list_2
    precision_val = total_correct_positive_matches / (total_correct_positive_matches + false_positives)
    recall_val = total_correct_positive_matches / (total_correct_positive_matches + false_negatives)
    f1score_val = (2 * precision_val * recall_val) / (precision_val + recall_val)

    metrics_dict = OrderedDict()

    metrics_dict = {'precision': precision_val,
                    'recall': recall_val,
                    'f1_score': f1score_val}

    metrics_df = pd.DataFrame.from_dict(metrics_dict, orient='index')
    metrics_df = metrics_df.rename(columns={0:'Results'})


    # Dictionary of DataFrames for Excel File
    dataframes_for_excel = {'model_vs_truths': test_vs_golden_compare,
                            'truths_not_in_model': missing_golden_matches,
                            'model_not_in_truths': matches_not_in_golden,
                            'all_metrics': metrics_df}

    return dataframes_for_excel


def tagger_vs_ground_truths(file1, field_rec_id=None, field_raw_address='Single String Address', to_standardize=True, missing_cols=missing_columns_from_file, ground_truth_cols=ground_truth_columns):

    # Create Dataframe from Raw Files
    test_file = pd.read_excel(file1, keep_default_na=False, dtype=str)

    # Add Record_ID to Dataframe if field_rec_id = None
    test_file = stndrdzr.record_id_addition(test_file, field_rec_id)

    # Add Empty Missing Columns to Dataframe
    test_file = stndrdzr.empty_column_addition(test_file, missing_cols)

    # Initiate Tagger
    tagger = crf.AddressTagger()

    # Tag Addresses
    tagged_test_file = tagger.series_to_address_df(test_file[field_raw_address], standardize=to_standardize)

    # Compare Tagger Results to Ground Truths
    tagger_ground_truths_dict = __pvt_tag_vs_ground_truths(tagged_test_file, test_file, ground_truth_cols)

    return tagger_ground_truths_dict


def tag_and_compare_addresses(file1, file2, groundtruths = None, field_rec_id = None, field_raw_address = 'Single String Address', to_standardize = True, run_mode = 'comparer', missing_cols = missing_columns_from_file, groundtruth_matchtypes=["Exact", "Standardized Exact"], matchtype = 'exact_match', threshold = 0.95):

    # Create Dataframe from Raw Files
    raw_address_list_1 = pd.read_excel(file1, keep_default_na=False, dtype=str)
    raw_address_list_2 = pd.read_excel(file2, keep_default_na=False, dtype=str)

    # Add the Record_ID field if field_rec_id is None
    raw_address_list_1 = stndrdzr.record_id_addition(raw_address_list_1, field_rec_id)
    raw_address_list_2 = stndrdzr.record_id_addition(raw_address_list_2, field_rec_id)

    # Add missing columns (City, State, Zip) to the Dataframes
    raw_address_list_1 = stndrdzr.empty_column_addition(raw_address_list_1, missing_cols)
    raw_address_list_2 = stndrdzr.empty_column_addition(raw_address_list_2, missing_cols)

    # Initiate the Address Tagger
    at = crf.AddressTagger()

    # Tag the 2 address lists
    tagged_address_list_1 = at.series_to_address_df(raw_address_list_1[field_raw_address], standardize=to_standardize)
    tagged_address_list_2 = at.series_to_address_df(raw_address_list_2[field_raw_address], standardize=to_standardize)

    # Compare the 2 tagged address lists
    compared_lists_dict = __pvt_compare_2_address_lists(raw_address_list_1, raw_address_list_2, tagged_address_list_1, tagged_address_list_2, run_mode, to_standardize, matchtype, threshold)

    # Model Results vs. Ground Truths
    if (run_mode == 'comparer_truths'):
        if matchtype != 'exact_match':
            groundtruth_matchtypes=["Exact", "Standardized Exact","Inexact"]
        model_comps_vs_truths_dict = __pvt_address_compare_vs_ground_truths(groundtruths, compared_lists_dict, groundtruth_matchtypes)
    else:
        model_comps_vs_truths_dict = dict()

    return compared_lists_dict, model_comps_vs_truths_dict



def tag_vs_truths_and_compare_addresses(file1, file2, groundtruths, field_rec_id = None, field_raw_address = 'Single String Address', to_standardize = True, run_mode = 'all', missing_cols = missing_columns_from_file, ground_truth_cols = ground_truth_columns, groundtruth_matchtypes=["Exact", "Standardized Exact"], matchtype = 'exact_match', threshold = 0.95):

    # Create Dataframe from Raw Files
    raw_address_list_1 = pd.read_excel(file1, keep_default_na=False, dtype=str)
    raw_address_list_2 = pd.read_excel(file2, keep_default_na=False, dtype=str)


    # Add the Record_ID field if field_rec_id is None
    raw_address_list_1 = stndrdzr.record_id_addition(raw_address_list_1, field_rec_id)
    raw_address_list_2 = stndrdzr.record_id_addition(raw_address_list_2, field_rec_id)

    # Add missing columns (City, State, Zip) to the Dataframes
    raw_address_list_1 = stndrdzr.empty_column_addition(raw_address_list_1, missing_cols)
    raw_address_list_2 = stndrdzr.empty_column_addition(raw_address_list_2, missing_cols)

    # Initiate the Address Tagger
    at = crf.AddressTagger()

    # Tag the 2 address lists
    tagged_address_list_1 = at.series_to_address_df(raw_address_list_1[field_raw_address], standardize=to_standardize)
    tagged_address_list_2 = at.series_to_address_df(raw_address_list_2[field_raw_address], standardize=to_standardize)

    # Compare Tagger Results to Ground Truths
    tagger_ground_truths_dict_file1 = __pvt_tag_vs_ground_truths(tagged_address_list_1, raw_address_list_1)
    tagger_ground_truths_dict_file2 = __pvt_tag_vs_ground_truths(tagged_address_list_2, raw_address_list_2)

    # Compare the 2 tagged address lists
    compared_lists_dict = __pvt_compare_2_address_lists(raw_address_list_1, raw_address_list_2, tagged_address_list_1, tagged_address_list_2, run_mode, to_standardize, matchtype, threshold)

    # Model Results vs. Ground Truths
    if matchtype != 'exact_match':
        groundtruth_matchtypes = ["Exact", "Standardized Exact", "Inexact"]
    model_comps_vs_truths_dict = __pvt_address_compare_vs_ground_truths(groundtruths, compared_lists_dict, groundtruth_matchtypes)

    return tagger_ground_truths_dict_file1, tagger_ground_truths_dict_file2, compared_lists_dict, model_comps_vs_truths_dict
