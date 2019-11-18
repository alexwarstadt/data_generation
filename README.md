# data_generation

OVERVIEW

This project includes utilities and scripts for automatic dataset generation. It is used in the following papers:

Kann, K., Warstadt, A., Williams, A., & Bowman, S. R. (2018). Verb argument structure alternations in word and sentence embeddings. arXiv preprint arXiv:1811.10773.

Warstadt, A., Cao, Y., Grosu, I., Peng, W., Blix, H., Nie, Y., ... & Wang, S. F. (2019). Investigating BERT's Knowledge of Language: Five Analysis Methods with NPIs. arXiv preprint arXiv:1909.02597.


PROJECT STRUCTURE

A shared vocabulary is vocabulary.csv to be read by the code.

The utils package contains shared functionality for reading the vocab and accessing fields.

The generation_projects package contains scripts for specific generated datasets.


VOCABULARY

The vocabulary lives in vocabulary.csv.

If you add a new column, you must update utils/data_type.py.

If you add a new row, definitely fill out all the relevant selectional restrictions.

Selectional restrictions are written in disjunctive normal form:
    A single condition is written as LABEL=VALUE.
    The symbol ";" is used for disjunction.
    The symbol "^" is used for conjunction.
    The entire selectional restriction should be written in the from a1^...^an;...;z1^...^zn. This matches any vocab
    item which matches conditions all of a1, ...., and an, OR ..., OR all of z1, ..., and zn


UTILS
utils.conjugate includes functions which conjugate verbs and add selecting auxiliaries/modals
utils.constituent_building includes functions which "do syntax":
    - build a subject relative clause from a head (subject_relative_clause)
    - gather all arguments of a verb (verb_args_from_verb)
utils.data_type contains the all-important data_type necessary for the numpy structured array data structure used in the vocabulary
utils.string_utils contains functions for modifying strings
utils.vocab_table contains functions for creating and accessing the vocabulary table
    - get_all gathers all vocab items with a given restriction
    - get_all_conjunctive gathers all vocab items with the given restrictions


DOCUMENTATION
Within each project's output directory, there is (should be) a docs document which explains:
    - the metadata in the output file
    - the data paradigm


GENERATION PROJECTS
long distance
npi
plurality
structure dependence
