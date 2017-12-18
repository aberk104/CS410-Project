import pycrfsuite
import pandas as pd
import json
from address_compare.feature_extraction import WordFeatures2 as wf
from collections import OrderedDict
from numpy.random import uniform, seed
from importlib import reload
from address_compare.constants import DIRECTIONS, STREET_TYPES, UNIT_TYPES
from string import punctuation
from address_compare.feature_extraction import FeatureExtractor, WordFeatures2, FullAddressFeatures
import numpy as np
import re
from address_compare.parsers import omit_hyphens

seed(1729)
training_size = 0.7  # use 70% for training

trainer2 = pycrfsuite.Trainer()

group = []

with open('data/tagged_addresses.json') as f:
    td = json.load(f)

wf = WordFeatures2()
fa = FullAddressFeatures()
<<<<<<< HEAD
fe = FeatureExtractor(tokenizer=omit_hyphens, lags = 0, leads = 0)
=======
fe = FeatureExtractor(lags = 1, leads = 1)
>>>>>>> master

for item in td:
    g = int(uniform() < training_size)
    features = fe.extract_features_from_string(item['raw_address'])
    # if len(features) != len(item['tags']): print(item['tokens'])
    trainer2.append(xseq = features, yseq = item['tags'], group=g)
    group.append(g)

trainer2.train('address_compare/trained_models/model4', holdout=0)

tagger3 = pycrfsuite.Tagger()
tagger3.open('address_compare/trained_models/model4')
test_group = [d for g, d in zip(group, td) if g == 0]
predicted = [tagger3.tag(fe.extract_features_from_token_list(t['tokens'])) for t in test_group]
print(json.dumps([(t['raw_address'], fe.extract_features_from_token_list(t['tokens']), t['tags'], p) for t, p in zip(test_group, predicted) if t['tags'] != p],indent=2))

<<<<<<< HEAD
print(tagger3.tag(fe.extract_features_from_string("#5 433 10TH AVE")))
from address_compare.tagging import AddressTagger
at = AddressTagger()
print(at.tag("#5 433 10TH AVE"))


# trainer2 = pycrfsuite.Trainer()
#
# for item in td:
#     g = int(uniform() < training_size)
#     features = fe.extract_features_from_token_list(item['tokens'])
#     if len(features) != len(item['tags']): print(item['tokens'])
#     trainer2.append(xseq = features, yseq = item['tags'], group=g)
#     group.append(g)

#
# trainer2.train('address_compare/trained_models/model4')

