'''
The address_randomizer will create a specified number of random raw addresses that can be used for testing purposes
'''

import pandas as pd
import random

available_unit_types = ['APT','BLDG','STE','FL','PH','UNIT',""]
available_street_types = ['RD','DR','AVE','LN','BLVD','PKWY',""]
available_street_names = ['MAPLE','ELM','MAIN','WALL','BROAD','GEORGE ALLEN','FULTON']
available_directionals = ['E','S','N','W',""]
available_unit_nums = ['1','2','3','4','5','6']

def random_addresses(num_addresses: int):
    '''
    This creates a random list of raw addreses that can be used for testing purposes
    :param num_addresses: this is an integer containing the number of addresses the user wants to create
    :return: new_address_df - a single column dataframe where the column name is "Single String Address" and the values are the randomized raw addresses
    '''
    new_addresses = list()

    for num in range(num_addresses):
        address = None
        unit_type = None
        unit_num = None
        pre_directional = None
        post_directional = None

        if random.choice([True,False]):
            unit_type = random.choice(available_unit_types)
            unit_num = random.choice(["#","","","","","",""]) + random.choice(available_unit_nums)

        if random.choice([True, False]):
            pre_directional = random.choice(available_directionals)

        if random.choice([True, False]):
            post_directional = random.choice(available_directionals)

        street_num = str(random.randint(1, 21))
        street_name = random.choice(available_street_names)
        street_type = random.choice(available_street_types)

        address_formats = {
            1: [unit_type, unit_num, random.choice(["-","","","","","",""]) if unit_num != None else "", street_num, pre_directional, street_name, post_directional, street_type],
            2: [street_num, pre_directional, street_name, post_directional, street_type, random.choice([",","","","","","",""]) if unit_num != None else "", unit_type, unit_num]}

        selected_format = random.randint(1,2)

        for item in address_formats[selected_format]:
            if item != None:
                if address == None and len(item) > 0:
                    address = item
                elif len(item) > 0:
                    address += str(" ") + item
        address = str.replace(address," ,",",") if random.choice([True,False]) else address
        new_addresses.append(address)

    new_address_df = pd.DataFrame(data=new_addresses, columns=['Single String Address'])

    return new_address_df