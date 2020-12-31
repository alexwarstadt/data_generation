import random
import math
import numpy as np

def decision(probability):
    return random.random() < probability

def subset(set, probability):
    np.random.shuffle(set)
    return set[:math.floor(len(set) * probability)]

def choice(set, avoid=[], avoid_add=None):
    """
    :param set: a set of vocab entries
    :param avoid: list of vocab entries to avoid sampling
    :param avoid_add: list of vocab entries to avoid sampling that will be updated to include newly sampled entry
    :return: a random element from the set
    """
    if avoid_add is not None:
        to_return = random.choice(np.setdiff1d(set, avoid_add))
        avoid_add.append(to_return.copy())
        return to_return
    else:
        return random.choice(np.setdiff1d(set, avoid))
