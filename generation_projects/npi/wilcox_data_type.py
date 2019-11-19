# These are the columns in the Wilcox et al. (2019) CSV.
# This data structure is required by the numpy ndarray.
# The first value is the name of the field (case sensitive!)
# The second value is the encoding the data in that field. "U" is for unicode, the number marks the max number of characters.

data_type = [("NonNegativeLicensor", "U100000"),
             ("NegativeLicensor", "U100000"),
             ("Subject", "U100000"),
             ("DistractorRC", "U100000"),
             ("RC", "U100000"),
             ("Aux", "U100000"),
             ("Ever", "U100000"),
             ("Verb", "U100000"),
             ("Any", "U100000"),
             ("Noun", "U100000"),
             ("Continuation", "U100000"),
             ("Conclusion", "U100000")]