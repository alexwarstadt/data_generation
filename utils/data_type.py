# These are the columns in the vocab table.
# This data structure is required by the numpy ndarray.
# The first value is the name of the field (case sensitive!)
# The second value is the encoding the data in that field. "U" is for unicode, the number marks the max number of characters.

data_type = [("expression", "U20"),
             ("category", "U20"),
             ("category_2", "U20"),
             ("animate", "U1"),
             ("occupation", "U1"),
             ("clothing", "U1"),
             ("appearance", "U1"),
             ("thing", "U1"),
             ("sg", "U1"),
             ("pl", "U1"),
             ("mass", "U1"),
             ("finite", "U1"),
             ("bare", "U1"),
             ("pres", "U1"),
             ("ing", "U1"),
             ("en", "U1"),
             ("3sg", "U1"),
             ("subj", "U20"),
             ("obj", "U20"),
             ("inflection", "U20"),
             ("root", "U20"),
             ("adjs", "U100"),
             ("restrictor_N", "U100"),
             ("restrictor_DE", "U100"),
             ("scope_DE", "U100")
            ]
