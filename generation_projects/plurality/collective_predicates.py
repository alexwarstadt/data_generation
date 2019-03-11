from utils.vocab_table import *
import random
# initialize output file
# output = open("../outputs/plurals/collectivepredicates.tsv", "w")
output = open("collectivepredicates.tsv", "w")
# set total number of paradigms to generate
number_to_generate = 1000
sentences = set()

# gather word classes that will be accessed frequently
all_irregular_nouns = get_all_conjunctive([("category", "N"), ("irrpl", "1")])
all_irregular_nouns_sg = get_all("sg", "1", all_irregular_nouns)
all_irregular_nouns_pl = get_all("pl", "1", all_irregular_nouns)
# all_collective_predicates = get_all_conjunctive(["category", ""], ["collective_pred", ""])

