# Authors: Alex Warstadt
# Functions for manipulating strings
import re

def remove_extra_whitespace(string):
    string = re.sub(' +', ' ', string).strip()
    string = re.sub(' \.', '.', string)
    string = re.sub(' ,', ',', string)
    string = re.sub(' \?', '?', string)
    return string

def string_beautify(string):
    string = remove_extra_whitespace(string)
    string = list(string)
    string[0] = string[0].capitalize()
    string = "".join(string)
    return string

