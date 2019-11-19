import random
import math
import numpy as np

def decision(probability):
    return random.random() < probability

def subset(set, probability):
    np.random.shuffle(set)
    return set[:math.floor(len(set) * probability)]

def choice(set, avoid=np.array([])):
    """
    :param set: a set of vocab entries
    :param avoid: list of vocab entries to avoid sampling
    :return: a random element from the set
    """
    return random.choice(np.setdiff1d(set, avoid))
