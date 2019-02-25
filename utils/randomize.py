import random
import math
import numpy as np


def decision(probability):
    return random.random() < probability

def subset(set, probability):
    np.random.shuffle(set)
    return set[:math.floor(len(set) * probability)]