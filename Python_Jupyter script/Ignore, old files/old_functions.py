import math
from random import Random

def rejection_sampling(probability_distribution):
    member_count = len(probability_distribution)
    step_size = 1.00 / (member_count * 1.00)

    accept = False
    r_value = 0

    while not accept:
        # generate r_temp and use it to determine R:
        random_generator = Random()
        r_temporal = random_generator.random()

        random_ceil = math.ceil(r_temporal / step_size)
        binned_object = probability_distribution[random_ceil - 1]
        r_value = binned_object['value']
        r_probability = binned_object['probability']

        # now, after we have R (r_value), draw S:
        s = random_generator.random()

        # accept or reject this observation:
        if s <= r_probability:
            accept = True
        else:
            accept = False

    return r_value