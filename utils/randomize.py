import random
import math
import numpy as np


def decision(probability):
    return random.random() < probability

def subset(set, probability):
    np.random.shuffle(set)
    return set[:math.floor(len(set) * probability)]

def choice(set, avoid=np.array([])):
    return random.choice(np.setdiff1d(set, avoid))
