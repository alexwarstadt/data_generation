# Authors: Alex Warstadt
# Functions for manipulating strings
import re

def remove_extra_whitespace(string):
    return re.sub(' +', ' ', string).strip()

def string_beautify(string):
    return remove_extra_whitespace(string).capitalize()

