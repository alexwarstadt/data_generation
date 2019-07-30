# Authors: Alex Warstadt
# Functions for manipulating strings
import re

def remove_extra_whitespace(string):
    string = re.sub(' +', ' ', string).strip()
    string = re.sub(' \.', '.', string)
    return string

def string_beautify(string):
    return remove_extra_whitespace(string).capitalize()

