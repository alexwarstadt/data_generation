# Author: Alex Warstadt
# Script for generating Chomsky's "structure dependent" sentences for QP1

from utils.conjugate import *
from random import choice
from utils.string_utils import remove_extra_whitespace
from utils.constituent_building import verb_args_from_verb


# initialize output file
rel_output_path = "outputs/long_distance/aux_agreement.tsv"
project_root = "/".join(os.path.join(os.path.dirname(os.path.abspath(__file__))).split("/")[:-2])
output = open(os.path.join(project_root, rel_output_path), "w")

# set total number of sentences to generate
number_to_generate = 10
sentences = set()

# gather word classes that will be accessed frequently
all_auxiliaries = get_all("category", "(S\\NP)/(S[bare]\\NP)")
all_nonfinite_transitive_verbs = get_all_conjunctive([("category", "(S\\NP)/NP"), ("finite", "0")])



# sample sentences until desired number
while len(sentences) < number_to_generate:
    # Aux                   DP1     V       DP2
    # is/#have/#did/#should the man eating a pie?

    # DP1     Aux                   V       DP2
    # the man is/#have/#did/#should eating a pie.

    V = choice(all_nonfinite_transitive_verbs)
    V_form = "bare" if V["bare"] == "1" else "ing" if V["ing"] == "1" else "en"
    args = verb_args_from_verb(V)
    DP1 = args["subject"]
    DP2 = args["object"]

    for Aux in all_auxiliaries:
        sentence_1 = "%s %s %s %s?" % (Aux[0], DP1[0], V[0], DP2[0])
        sentence_2 = "%s %s %s %s." % (DP1[0], Aux[0], V[0], DP2[0])
        acceptability = 1 if is_match_disj(V, Aux["arg_2"]) else 0
        output.write("%s\t%d\t\t%s\n" %
                     ("exp=long_distance-condition=aux_agreement-aux=%s-verb_form=%s-fronted=1-separation=%d" % (Aux[0], V_form, len(DP1[0])),
                      acceptability,
                      sentence_1))
        output.write("%s\t%d\t\t%s\n" %
                     ("exp=long_distance-condition=aux_agreement-aux=%s-verb_form=%s-fronted=0-separation=0" % (Aux[0], V_form),
                      acceptability,
                      sentence_2))
        sentences.add(sentence_1)
