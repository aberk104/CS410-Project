'''
The address_randomizer will create a specified number of random raw addresses that can be used for testing purposes
'''

import pandas as pd
import random
from itertools import combinations
from numpy import random as npr

available_unit_types = ['APT','BLDG','STE','FL','PH','UNIT',""]
available_street_types = ['RD','DR','AVE','LN','BLVD','PKWY',""]
available_street_names = ['MAPLE','ELM','MAIN','WALL','BROAD','GEORGE ALLEN','FULTON',
                          'KING GEORGE', 'A', 'B', 'C', 'TWELVE OAKS', "MARTIN LUTHER KING JR.",
                          'CALIFORNIA']
available_directionals = ['E','S','N','W','NE','NW','SE','SW',""*5]
available_unit_nums = ['1','2','3','4','5','6']
address_formats_with_unit = [
    "#{UNIT_NUMBER}, {STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}"
    "{UNIT_TYPE} {UNIT_NUMBER} - {STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}",
    "{UNIT_TYPE} {UNIT_NUMBER}, {STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}",
    "{STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}, {UNIT_TYPE} {UNIT_NUMBER}",
    "{UNIT_NUMBER} - {STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}"
]

def random_addresses(num_addresses: int, raw_address_col_name = 'Single String Address'):
    '''
    This creates a random list of raw addreses that can be used for testing purposes
    :param num_addresses: this is an integer containing the number of addresses the user wants to create
    :param raw_address_col_name: this represents the name of the column for the raw addresses.  it will default to 'Single String Address' if not passed in
    :return: new_address_df - a single column dataframe where the column name is "Single String Address" and the values are the randomized raw addresses
    '''
    new_addresses = list()

    for num in range(num_addresses):
        address = None
        unit_type = None
        unit_num = None
        pre_directional = None
        post_directional = None

        if random.choice([True,False*4]):
            unit_type = random.choice(available_unit_types)
            unit_num = random.choice(["#",""*10]) + random.choice(available_unit_nums)

        if random.choice([True, False*4]):
            pre_directional = random.choice(available_directionals)

        if random.choice([True, False*4]):
            post_directional = random.choice(available_directionals)

        street_num = str(random.randint(1, 21))
        street_name = random.choice(available_street_names)
        street_type = random.choice(available_street_types)

        address_formats = {
            1: [unit_type, unit_num, random.choice(["-",""*10]) if unit_num != None else "", street_num, pre_directional, street_name, post_directional, street_type],
            2: [street_num, pre_directional, street_name, post_directional, street_type, random.choice([",",""*10]) if unit_num != None else "", unit_type, unit_num]}

        selected_format = random.randint(1,2)

        for item in address_formats[selected_format]:
            if item != None:
                if address == None and len(item) > 0:
                    address = item
                elif len(item) > 0:
                    address += str(" ") + item
        address = str.replace(address," ,",",") if random.choice([True,False]) else address
        new_addresses.append(address)

    new_address_df = pd.DataFrame(data=new_addresses, columns=[raw_address_col_name])

    return new_address_df


def random_unit_number():
    k = str(random.randint(1, 4000))
    return random.choice([k, 'A', 'B', 'C', 'D'])

def random_street_name():
    if random.random() < 0.5:
        return str(random.randint(1, 200))
    return random.choice(available_street_names)

def num_suffix(n):
    if not n.isdigit():
        return n
    return n + {"1": 'st', "2": 'nd', "3": 'rd',
                "4": 'th', "5": 'th', "6": 'th',
                "7": 'th', "8": 'th', "9": 'th',
                "0": 'th'}[n[-1]]

def random_address(unit_number:bool = True):
    address1 = {k: '' for k in ['UNIT_TYPE', 'UNIT_NUMBER', 'STREET_NUMBER',
                                'STREET_NAME', 'STREET_TYPE', 'PRE_DIRECTION', 'POST_DIRECTION']}

    address1['STREET_NUMBER'] = str(random.randint(1, 99999))
    address1['STREET_NAME'] = random_street_name()
    address1['STREET_TYPE'] = random.choice(available_street_types[:-1])
    direction = random.choice(['PRE_DIRECTION', 'POST_DIRECTION', ''])
    if direction:
        address1[direction] = random.choice(available_directionals[:-1])

    if unit_number:  # half with unit numbers
        address1['UNIT_NUMBER'] = random_unit_number()
        address1['UNIT_TYPE'] = random.choice(available_unit_types[:-1])
    return address1

def generate_typo(address):
    pass

def format_address(a, f):
    return f.format(**a).replace('  ', ' ').replace(' ,', ',')

def random_addresses2(n):
    # with unit numbers
    address_formats_with_unit = [
        "#{UNIT_NUMBER}, {STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}",
        "{UNIT_TYPE} {UNIT_NUMBER} - {STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}",
        "{UNIT_TYPE} {UNIT_NUMBER}-{STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}",
        "{UNIT_TYPE} {UNIT_NUMBER}, {STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}",
        "{STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}, {UNIT_TYPE} {UNIT_NUMBER}",
        "{UNIT_NUMBER} - {STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}"
    ]

    address_without_unit = "{STREET_NUMBER} {PRE_DIRECTION} {STREET_NAME} {STREET_TYPE} {POST_DIRECTION}"


    a1s = list()
    a2s = list()
    match = list()

    for i in range(n):
        format_combinations = combinations(address_formats_with_unit, 2)
        address = random_address(True)
        address2 = address.copy()
        address2['STREET_NAME'] = num_suffix(address['STREET_NAME'])
        for a1, a2 in format_combinations:
            a1s.append(format_address(address, a1))
            a2s.append(format_address(address, a2))
            match.append(True)
            if address != address2:
                a1s.append(format_address(address, a1))
                a2s.append(format_address(address2, a2))
                match.append(True)


        address2 = address.copy()
        address2["STREET_NAME"] = num_suffix(address2['STREET_NAME'])
        a1s.append(format_address(address, random.choice(address_formats_with_unit)))
        a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
        match.append(True)

        address2 = address.copy()
        address2["STREET_NUMBER"] = str(int(address["STREET_NUMBER"])+1)
        a1s.append(format_address(address, random.choice(address_formats_with_unit)))
        a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
        match.append(False)

        address2 = address.copy()
        address2["STREET_NUMBER"] = str((int(address["STREET_NUMBER"])/10) % 10000 +1)
        address2["STREET_NAME"] = num_suffix(address2["STREET_NAME"])
        a1s.append(format_address(address, random.choice(address_formats_with_unit)))
        a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
        match.append(False)

        address2 = address.copy()
        address2["UNIT_NUMBER"] = address['UNIT_NUMBER'] + str(random.randint(1, 9))
        a1s.append(format_address(address, random.choice(address_formats_with_unit)))
        a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
        match.append(False)

        address2 = address.copy()
        address2["STREET_NAME"] = num_suffix(address2["STREET_NAME"])
        address2["UNIT_NUMBER"] = address['UNIT_NUMBER'] + str(random.randint(1, 9))
        a1s.append(format_address(address, random.choice(address_formats_with_unit)))
        a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
        match.append(False)

        address2 = address.copy()
        while address2 == address:
            address2["STREET_NAME"] = random_street_name()
        a1s.append(format_address(address, random.choice(address_formats_with_unit)))
        a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
        match.append(False)

        address2 = address.copy()
        while address2 == address:
            address2["STREET_TYPE"] = random.choice(available_street_types[:-1])
        a1s.append(format_address(address, random.choice(address_formats_with_unit)))
        a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
        match.append(False)

        if address['PRE_DIRECTION'] or address['POST_DIRECTION']:
            address2 = address.copy()
            address2['PRE_DIRECTION'], address2['POST_DIRECTION'] = address['POST_DIRECTION'], address['PRE_DIRECTION']
            a1s.append(format_address(address, random.choice(address_formats_with_unit)))
            a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
            match.append(False)

        d = 'PRE_DIRECTION' if address['PRE_DIRECTION'] else 'POST_DIRECTION'
        address2 = address.copy()
        while address2 == address:
            address2[d] = random.choice(available_directionals)
        a1s.append(format_address(address, random.choice(address_formats_with_unit)))
        a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
        match.append(False)

        if address['STREET_NUMBER'] != address["UNIT_NUMBER"]:
            address2 = address.copy()
            address2['STREET_NUMBER'], address2['UNIT_NUMBER'] = address['UNIT_NUMBER'], address['STREET_NUMBER']
            a1s.append(format_address(address, random.choice(address_formats_with_unit)))
            a2s.append(format_address(address2, random.choice(address_formats_with_unit)))
            match.append(False)


        for j in range(4):
            address2 = random_address()
            match.append(address2 == address)
            a1s.append(format_address(address, random.choice(address_formats_with_unit)))
            a2s.append(format_address(address2, random.choice(address_formats_with_unit)))

    return pd.DataFrame.from_dict({'address_1': a1s, 'address_2': a2s, 'match': match})
