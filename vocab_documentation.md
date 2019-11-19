# Vocab documentation

OVERVIEW
- This document explains the purpose of each of the column headings in vocabulary.csv
- For details on the structure of the entries, see the README file

## expression
- each entry is a lexical expression
- entries can be more than one word, for example 'think about'

## category
- tag based on categorial grammar
- contains information about what the expression combines with
- for example, transitive verbs are '(S\NP)/NP' and intransitive verbs are 'S\NP'

## category2
- tag based on part of speech, sometimes with additional info
- for example, transitive verbs are 'TV' and intransitive verbs are 'IV'
- 'IV' labels can contain additional information about whether the subject needs to be agentive and/or plural
- note that this column is not complete for all expressions. It is only used when the information in 'category' is insufficient

## verb
- indicates whether the expression is a main verb
- value is 1 if the expression is a main verb, and blank otherwise
- this category does not mark auxiliary verbs (e.g., 'can', 'might') or copulas

## noun
- indicates whether the expression is a noun (N or NP)
- value is 1 if the expression is a noun, and blank otherwise
- this category includes proper nouns (e.g., 'The Great Lakes')
- this category includes expletive pronouns 'it' and 'there'
- this category DOES NOT include any other pronouns (e.g., 'him', non-expletive 'it')

## non_v_pred
- indicates whether the expression is a non-verbal-predicate
- used for predicative adjectives (e.g., 'unemployed', 'hidden')
- used for prepositional phrases (e.g., 'at the bottom of', 'in one piece')
- used for other predicative phrases (e.g., 'similar to')

##frequent
- indicates whether the expression is frequent in English
- frequency is based on annotators judgments
- value is 1 if frequent, 0 if infrequent
- only nouns, determiners, and adverbs are consistently marked for frequency
- some verbs may be marked for frequency
- many irregular plural nouns are marked as infrequent (e.g., 'radii')

## sg
- indicates whether an expression is singular or not
- value is 1 if singular, 0 if plural, blank if the expression is not a noun
- only nouns are marked for singular or plural
- mass nouns are marked as sg because the have singular agreement with verbs for which they are subjects
- expression like 'Galileo' and 'turtle' are marked singular

## pl
- indicates whether an expression is plural or not
- value is 1 if plural, 0 if singular, blank if the expression is not a noun
- only nouns are marked for singular or plural
- expressions like 'the Clintons' and 'turtles' are marked plural

## mass
- indicates whether an expression is a mass noun or not
- value is 1 if it's a mass noun, 0 if it's a count noun, and blank if the expression is not a noun
- only nouns are marked for whether they're mass
- expressions like 'science' and 'ice cream' are marked as mass nouns

## animate


## properNoun


## finite


## bare


## pres


## past


## ing


## en


## 3sg


## arg_1


## arg_2


## arg_3


## root


## wh_np_verb


## responsive


## passive


## strict_intrans


## strict_trans


## causative


## spray_load


## inchoative


## agentive


## event


## adjs


## restrictor_DE


## scope_DE


## NPI


## agent


## occupation


## clothing


## appearance


## physical


## conceptual


## breakable


## start_with_vowel


## frontable


## gender


## irrpl


## special_en_form


## irr_verb


## document


## negated


## locale


## institution


## arg_clause


## homophonous


## pluralform


## singularform


## sgequalspl


## topic


## image


## v_embed_sc


## change_of_state


## initial_state


## change_arg


## vehicle


## vegetable


## food


## light


## liquid


## animal


## openable


## climbable


## cleanable


## quantifier

