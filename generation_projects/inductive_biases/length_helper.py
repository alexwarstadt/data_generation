from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
from utils.exceptions import LengthHelperError
import random

class LengthHelper:
    def __init__(self):
        self.antecedents = []
        self.adverbs = get_all("category_2", "subordinating_conj")
        self.long_length = 20

    def build_dependent_clauses(self, main_clause, other_main_clause=None):
        for _ in range(10):
            adverb = choice(self.adverbs)[0]
            min_long_clause_length = self.long_length - min([len(main_clause.split()), len(other_main_clause.split())]) - len(adverb.split())
            max_short_clause_length = self.long_length - max([len(main_clause.split()), len(other_main_clause.split())]) - len(adverb.split()) - 1
            if min_long_clause_length < 13 and max_short_clause_length > 5:
                break
        if not (min_long_clause_length < 13 and max_short_clause_length > 5):
            raise LengthHelperError(main_clause, "")

        short_subordinate_clause = None
        short_sentences = list(filter(lambda x: len(x.split()) <= max_short_clause_length and x.startswith(adverb), self.antecedents))
        if len(short_sentences) > 0:
            short_subordinate_clause = choice(short_sentences)
        else:
            for _ in range(10):
                new_sentence = make_sentence(allow_recursion=True)[0]
                new_sentence_length = len(new_sentence.split())
                new_sentence = adverb + " " + new_sentence
                if new_sentence_length <= max_short_clause_length:
                    short_subordinate_clause = new_sentence
                    break
                else:
                    self.antecedents.append(new_sentence)
        if short_subordinate_clause is None:
            raise LengthHelperError(main_clause, "is too long")


        long_subordinate_clause = None
        long_sentences = list(filter(lambda x: len(x.split()) >= min_long_clause_length and x.startswith(adverb), self.antecedents))
        if len(long_sentences) > 0:
            long_subordinate_clause = choice(long_sentences)
        else:
            for _ in range(10):
                new_sentence = make_sentence(allow_recursion=True)[0]
                new_sentence_length = len(new_sentence.split())
                new_sentence = adverb + " " + new_sentence
                new_sentence_length = len(new_sentence.split())
                if new_sentence_length >= min_long_clause_length:
                    long_subordinate_clause = new_sentence
                    break
                else:
                    self.antecedents.append(new_sentence)
        if long_subordinate_clause is None:
            raise LengthHelperError(main_clause, "is too short")


        return long_subordinate_clause, short_subordinate_clause
