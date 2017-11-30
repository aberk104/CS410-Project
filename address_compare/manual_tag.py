# this script helps with manual tagging of lists of address strings.
# Not finished.

import pandas as pd
import argparse
from address_compare.parsers import hyphen_parse

parser = argparse.ArgumentParser()
parser.add_argument('data')

args = parser.parse_args()



english_tags = ["STREET_NUMBER", "STREET_NAME", "OCCUPANCY_NUMBER", "OCCUPANCY_IDENTIFIER",
                "DIRECTION"]

def tag(sentence):
    print(sentence)
    print('  ')
    parsed = hyphen_parse(sentence)
    for w in parsed:
        input("What is " + w)

if __name__ == '__main__':
    with open(args.data) as f:
        data = f.readlines()

    tag(data[0])