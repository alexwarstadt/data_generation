# data_generation

This project includes utilities for generating sentences with certain grammatical properties.


OVERVIEW

A shared vocabulary is kept in vocabulary.numbers, which must be exported to .csv to be read by the code.

The utils package contains shared functionality for reading the vocab and accessing fields.

The generation_projects package contains scripts for specific generated datasets.


VOCABULARY

The vocabulary should be edited in vocabulary.numbers. Once desired edits have been made, export to vocabulary.csv, as
the .numbers file cannot be read.

If you add a new column, you must update utils/data_type.py.

If you add a new row, definitely fill out all the relevant selectional restrictions.

Selectional restrictions are written in disjunctive normal form:
    A single condition is written as LABEL=VALUE.
    The symbol ";" is used for disjunction.
    The symbol "^" is used for conjunction.
    The entire selectional restriction should be written in the from a1^...^an;...;z1^...^zn. This matches any vocab
    item which matches conditions all of a1, ...., and an, OR ..., OR all of z1, ..., and zn


UTILS


GENERATION PROJECTS

