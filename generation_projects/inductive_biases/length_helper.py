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

    def build_dependent_clauses(self, main_clauses):
        for _ in range(10):
            adverb = choice(self.adverbs)[0]
            min_long_clause_length = self.long_length - min([len(x.split()) for x in main_clauses]) - len(adverb.split())
            max_short_clause_length = self.long_length - max([len(x.split()) for x in main_clauses]) - len(adverb.split()) - 1
            if min_long_clause_length < 10 and max_short_clause_length > 2:
                break
        if not (min_long_clause_length < 10 and max_short_clause_length > 2):
            raise LengthHelperError("\n".join(main_clauses), "")

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
            raise LengthHelperError("\n".join(main_clauses), "is too long")


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
            raise LengthHelperError("\n".join(main_clauses), "is too short")


        return long_subordinate_clause, short_subordinate_clause
