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

## frequent
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
- indicates whether a noun is animate or not
- value is 1 if yes, 0 if no, and blank if the expression is not a noun
- only nouns are marked

## properNoun
- indicates whether a noun is a proper name or not 
- value is 1 if yes, 0 if no, and blank if the expression is not a noun
- only nouns are marked

## finite
- indicatees whether a verb is finite, i.e. can stand alone as the main verb of a finite clause without an auxiliary present
- value is 1 if yes, 0 if no, and blank if the expression is not a verb
- only verbs are marked
- expressions like 'walks', 'fell asleep', or 'leave' are finite. Expressions like 'eaten' and 'proving' are not.

## bare
- indicatees whether a verb is in the bare form, i.e. infinitive without the marker 'to'
- value is 1 if yes, 0 if no, and blank if the expression is not a verb
- only verbs are marked

## pres
- indicatees whether a verb is in the simple present
- value is 1 if yes, 0 if no, and blank if the expression is not a verb
- only verbs are marked

## past
- indicatees whether a verb is in the simple past
- value is 1 if yes, 0 if no, and blank if the expression is not a verb
- only verbs are marked

## ing
- indicatees whether a verb is in the progressive
- value is 1 if yes, 0 if no, and blank if the expression is not a verb
- only verbs are marked

## en
- indicatees whether a verb is in the past participle
- value is 1 if yes, 0 if no, and blank if the expression is not a verb
- only verbs are marked

## 3sg
- indicatees whether a verb has 3rd person singular present morphology. 
- value is 1 if yes, 0 if no, and blank if the expression is not a verb
- only present verbs are marked

## arg_1
- specifies argument restrictions on the first argument of a functor expression
- For a verb, this is the subject
- For a determiner or adjective, it is the modified noun
- For a relational noun, it is (usually) a prepositional phrase
- For an auxiliary, it is the verb

## arg_2
- specifies argument restrictions on the 2nd most oblique argument
- For a verb, this is typically an object, prepositional object, clausal complement, etc.
  
## arg_3
- specifies argument restrictions on the 3rd most oblique argument

## root
- provides a string indicating which root a verb belongs to
- different morphological forms of the same lemma have share a root
- different argument structures of the same lemma have a different root

## wh_np_verb
- indicates whether a verb can take a wh-argument with an NP gap
- only verbs are marked
- Example: remember, as in "I remember what you ate"

## responsive
- indicates whether a verb can take a wh-argument with complementizer "whether"
- only verbs are marked
- Example: know, as in "I know whether he will come"

## passive
- indicates whether a verb can be passivized
- only some verbs are marked.
- If a verb is not marked, there is no guarantee that it can or cannot be passivized.
- Examples: "hire" can be passivized as in "He was hired by Walmart"

## strict_intrans
- indicates whether a verb is strictly intransitive, i.e. cannot appear with an object

## strict_trans
- indicates whether a verb is strictly transitive, i.e. must appear with an object

## causative
- indicates whether an intransitive verb can be used in a causative construction
- Only intransitive verbs are marked

## spray_load
- indicates whether a verb participates in the causative--inchoative alternation

## inchoative
- indicates whether a transitive verb can be used in an inchoative construction
- Only transitive verbs are marked

## agentive
- indicates whether a verb has an agentive subject

## event
- indicates whether a verb denotes an event

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

