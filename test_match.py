import pandas as pd
from address_compare.tagging import AddressTagger
from address_compare.prob_matchers import MatchClassifier

s1 = pd.Series(["#1401 750 Jervis Street", "25 West King Edward Avenue", "950 EAST 10TH AVE, Apt 1"])
s2 = pd.Series(["#750 1401 Jervis Street", "Unit 1, 950 E 10 AVE", "25 W King Edward Ave", '123 Fake Street'])
print(s1)
print(s2)

at = AddressTagger()
ad1 = at.series_to_address_df(s1)
ad2 = at.series_to_address_df(s2)

from address_compare.prob_matchers import ProbMatcher
pm = ProbMatcher()
print(pm.match_probabilities(ad1, ad2, -1))