'''
The matcher.py file contains a match function to compare 2 lists of addresses.
It calls the separate exact and learning compare comparers in order to find a matching address in list 2 for each address in list 1
'''

def match(address_list_1, address_list_2, compare_function):
    matched_pairs = list()
    address_list_1_copy = address_list_1.copy()

    address1_index = 0

    for address1 in address_list_1:
        address2_index = 0
        for address2 in address_list_2:
            if compare_function(address1, address2):
                matched_pairs.append((address1, address2)) #this will get changed to record IDs instead of the full orderedDict once record IDs become available
                address_list_2.pop(address2_index)
                address_list_1_copy.pop(address1_index)
                break
            address2_index += 1
        address1_index += 1

    unmatched_address_list_1 = list()
    for item in address_list_1_copy:
        unmatched_address_list_1.append((item, "NA")) #this will eventually get changed to Record IDs instead of the full orderedDict

    unmatched_address_list_2 = list()
    for item in address_list_2:
        unmatched_address_list_2.append((item, "NA")) #this will eventually get changed to Record IDs instead of the full orderedDict

    