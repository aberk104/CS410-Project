'''
This file contains aggregated functions to tag and match addresses
'''
import pandas as pd
from address_compare import standardizers as stndrdzr
from address_compare import crf_tagger as crf
from address_compare import matcher as mtch
from collections import OrderedDict
import sklearn


missing_columns_from_file = ['CITY', 'STATE', 'ZIP_CODE', 'UNKNOWN']
ground_truth_columns = ['Record_ID', 'Tagged Street Number', 'Tagged Pre Street Direction', 'Tagged Street Name',
                        'Tagged Street Type', 'Tagged Post Street Direction', 'Tagged Unit Type',
                        'Tagged Unit Number']

def tagger_vs_ground_truths(file, field_rec_id, field_raw_address, to_standardize, missing_cols = missing_columns_from_file, ground_truth_cols = ground_truth_columns):
    test_file = pd.read_excel(file, keep_default_na=False, dtype=str)
    test_file = stndrdzr.record_id_addition(test_file, field_rec_id)

    # Add Empty Missing Columns to Dataframe
    test_file = stndrdzr.empty_column_addition(test_file, missing_cols)

    tagger = crf.AddressTagger()
    tagged_test_file = tagger.series_to_address_df(test_file[field_raw_address], standardize=to_standardize)
    crf_tagged_test_file = tagged_test_file.join(test_file['Record_ID'])

    manual_tagged_test_file = test_file[ground_truth_cols].copy()
    manual_tagged_test_file = manual_tagged_test_file.rename(columns={'Tagged Street Number': 'STREET_NUMBER',
                                                                      'Tagged Pre Street Direction': 'PRE_DIRECTION',
                                                                      'Tagged Street Name': 'STREET_NAME',
                                                                      'Tagged Street Type': 'STREET_TYPE',
                                                                      'Tagged Post Street Direction': 'POST_DIRECTION',
                                                                      'Tagged Unit Type': 'UNIT_TYPE',
                                                                      'Tagged Unit Number': 'UNIT_NUMBER'})

    cols_for_matcher = ['UNIT_TYPE', 'UNIT_NUMBER', 'STREET_NUMBER', 'PRE_DIRECTION', 'STREET_NAME', 'STREET_TYPE',
                        'POST_DIRECTION']
    correctly_tagged_addresses = mtch.exact_matcher(crf_tagged_test_file, manual_tagged_test_file, cols_for_matcher)

    incorrectly_tagged_addresses = crf_tagged_test_file.mask(crf_tagged_test_file.Record_ID.isin(correctly_tagged_addresses['Record_ID_list_1'])).dropna()
    incorrectly_tagged_addresses = incorrectly_tagged_addresses.merge(test_file[ground_truth_cols], on='Record_ID')

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
        precision, recall, fscore, ignore = sklearn.metrics.precision_recall_fscore_support(
            manual_tagged_test_file[col], crf_tagged_test_file[col], average='micro')
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
    dataframes_for_tagger_excel = {'test_data_file': test_file,
                                   'crf_tagged_output': tagged_test_file,
                                   'crf_output_w_id': crf_tagged_test_file,
                                   'ground_truth_test_file': manual_tagged_test_file,
                                   'correctly_tagged': correctly_tagged_addresses,
                                   'incorrectly_tagged': incorrectly_tagged_addresses,
                                   'tagger_metrics': metrics_df}

    return dataframes_for_tagger_excel


def tagger_and_comparer(file1, file2, field_rec_id, field_raw_address, to_standardize, missing_cols = missing_columns_from_file):
    raw_address_list_1 = stndrdzr.record_id_addition(file1, field_rec_id)
    raw_address_list_2 = stndrdzr.record_id_addition(file2, field_rec_id)

    raw_address_list_1 = stndrdzr.empty_column_addition(raw_address_list_1, missing_cols)
    raw_address_list_2 = stndrdzr.empty_column_addition(raw_address_list_2, missing_cols)

    at = crf.AddressTagger()

    tagged_address_list_1 = at.series_to_address_df(raw_address_list_1[field_raw_address], standardize=to_standardize)
    tagged_address_list_2 = at.series_to_address_df(raw_address_list_2[field_raw_address], standardize=to_standardize)

    raw_address_list_1 = stndrdzr.fix_cities_zips(raw_address_list_1)
    raw_address_list_2 = stndrdzr.fix_cities_zips(raw_address_list_2)