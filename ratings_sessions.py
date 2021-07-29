import random


class COMPARE_TYPE(object):
    DIRECT = 0
    MULTI = 1
    RATE = 2
    TWO_VIBE = 3


num_types = 4


def get_types_direct_primary():
    val = random.randint(0, 3)

    session_length = 60
    group_length_ranges = (int(6/2), int(14/2))

    ### 6-14
    ### //

    group_lengths = []
    length = 100
    for i in range(0, length):
        cur_length = random.randint(group_length_ranges[0], group_length_ranges[1])*2
        print(cur_length)
        group_lengths.append(cur_length)

        if sum(group_lengths) >= 50:
            break

    types_to_do = []
    for gl in group_lengths:
        if val == 0:
            selection = random.randint(1, 2) + 1  # skips multi
        else:
            selection = 0

        for i in range(gl):
            types_to_do.append(selection)

    return types_to_do

