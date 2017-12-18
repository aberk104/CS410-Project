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
from address_compare.parsers import omit_hyphen

seed(1729)
training_size = 0.8  # use 70% for training

trainer = pycrfsuite.Trainer()
trainer.select('ap')

group = []

with open('data/tagged_addresses.json') as f:
    td = json.load(f)

wf = WordFeatures2()
fa = FullAddressFeatures()
fe = FeatureExtractor(tokenizer=omit_hyphen,lags = 0, leads = 0)

for item in td:
    g = int(uniform() < training_size)
    features = fe.extract_features_from_string(item['raw_address'])
    # if len(features) != len(item['tags']): print(item['tokens'])
    trainer.append(xseq = features, yseq = item['tags'], group=g)
    group.append(g)

trainer.train('address_compare/trained_models/model4', holdout=0)

tagger = pycrfsuite.Tagger()
tagger.open('address_compare/trained_models/model4')
test_group = [d for g, d in zip(group, td) if g == 0]
predicted = [tagger.tag(fe.extract_features_from_string(t['raw_address'])) for t in test_group]
print(json.dumps([(t['raw_address'], t['tags'], p, fe.extract_features_from_string(t['raw_address'])) for t, p in zip(test_group, predicted) if t['tags'] != p],indent=2))

trainer2 = pycrfsuite.Trainer()

for item in td:
    g = int(uniform() < training_size)
    features = fe.extract_features_from_token_list(item['tokens'])
    if len(features) != len(item['tags']): print(item['tokens'])
    trainer2.append(xseq = features, yseq = item['tags'], group=g)
    group.append(g)

# trainer2.train('address_compare/trained_models/model4')
