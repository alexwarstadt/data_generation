from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random

class MyGenerator(data_generator.InductiveBiasesGenerator):
    def __init__(self):
        super().__init__(uid="person_control",
                         linguistic_feature_type="morphological",
                         linguistic_feature_description="Is the pronoun 1st person?",
                         surface_feature_type=None,
                         surface_feature_description=None,
                         control_paradigm=True)

        animate = get_all("animate", "1")
        self.nom_pronoun = get_all("category_2", "nom_pronoun", animate)
        self.acc_pronoun = get_all("category_2", "acc_pronoun", animate)
        self.poss_det = get_all("category_2", "poss_det", animate)
        self.poss_pronoun = get_all("category_2", "poss_pronoun", animate)
        self.first = get_all("person", "1")
        self.safe_verbs = get_all("ing", "0", all_verbs)   # This is because auxiliaries "be" and "have" for 1st and 2nd person not implemented
        self.cp_verb = get_all("category", "(S\\NP)/S", self.safe_verbs)
        self.trans_verb = np.intersect1d(self.safe_verbs, all_anim_anim_verbs)
        self.dets = get_all("category_2", "D")
        self.possessible_animates = get_all("category", "N\\NP[poss]")

    def sample(self):
        # Training 1
        # I     think         that    John found  the cat.
        # first cp_verb_first THAT D1 NP1  verb_1 D2  NP2

        # Training 0
        # They      think             that    John found  the cat.
        # non_first cp_verb_non_first THAT D1 NP1  verb_1 D2  NP2

        # Test 1
        #    John thinks    that the cat found  me.
        # D1 NP1  cp_verb_1 THAT D2  NP2 verb_2 first_acc

        # Test 0
        #    John thinks    that the cat found  them.
        # D1 NP1  cp_verb_1 THAT D2  NP2 verb_2 non_first_acc

        r = random.random()
        if r < 0:  # nominative pronoun
            first = choice(np.intersect1d(self.first, self.nom_pronoun))
            non_first = choice(np.setdiff1d(self.nom_pronoun, self.first))
            first_acc = choice(get_all_conjunctive([("person", first["person"]), ("sg", first["sg"])], self.acc_pronoun))
            non_first_acc = choice(get_all_conjunctive([("person", non_first["person"]), ("sg", non_first["sg"])], self.acc_pronoun))
        elif r < 1/2:   # possessive det
            noun = choice(self.possessible_animates)
            first_det = choice(get_all("person", "1", self.poss_det))
            first = noun.copy()
            first[0] = first_det[0] + " " + first[0]
            non_first_det = choice(np.setdiff1d(self.poss_det, self.first))
            non_first = noun.copy()
            non_first[0] = non_first_det[0] + " " + non_first[0]
            first_acc = choice(get_all_conjunctive([("person", first_det["person"]), ("sg", first_det["sg"])], self.acc_pronoun))
            non_first_acc = choice(get_all_conjunctive([("person", non_first_det["person"]), ("sg", non_first_det["sg"])], self.acc_pronoun))
        else:   # possessive pronoun
            first = choice(get_all("person", "1", self.poss_pronoun))
            non_first = choice(np.setdiff1d(self.poss_pronoun, self.first))
            first_acc = choice(get_all_conjunctive([("person", first["person"]), ("sg", first["sg"])], self.acc_pronoun))
            non_first_acc = choice(get_all_conjunctive([("person", non_first["person"]), ("sg", non_first["sg"])], self.acc_pronoun))
            vals = ["1", "0"]
            sg = random.choice(["1", "0"])  # Possessive pronouns can have either singular or plural agreement, irrespective of person/number marking
            vals.remove(sg)
            pl = vals[0]
            first["sg"] = sg
            first["pl"] = pl
            non_first["sg"] = sg
            non_first["pl"] = pl

        NP1 = choice(all_animate_nouns)
        NP2 = choice(all_animate_nouns, avoid=NP1)
        D1 = choice(get_matched_by(NP1, "arg_1", self.dets))
        D2 = choice(get_matched_by(NP2, "arg_1", self.dets))
        cp_verb = choice(self.cp_verb)
        cp_verb_aux = return_aux(cp_verb, first)
        cp_verb_first = re_conjugate(cp_verb, first, cp_verb_aux)
        cp_verb_non_first = re_conjugate(cp_verb, non_first, cp_verb_aux)
        cp_verb_1 = re_conjugate(cp_verb, NP1, cp_verb_aux)
        verb = choice(self.trans_verb)
        verb_aux = return_aux(verb, NP1)
        verb_1 = re_conjugate(verb, NP1, verb_aux)
        verb_2 = re_conjugate(verb, NP2, verb_aux)

        track_sentence = "%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0])

        data = self.build_paradigm(
            training_1_1="%s %s that %s %s %s %s %s" % (first[0], cp_verb_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            training_0_0="%s %s that %s %s %s %s %s" % (non_first[0], cp_verb_non_first[0], D1[0], NP1[0], verb_1[0], D2[0], NP2[0]),
            test_1_0="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], first_acc[0]),
            test_0_1="%s %s %s that %s %s %s %s" % (D1[0], NP1[0], cp_verb_1[0], D2[0], NP2[0], verb_2[0], non_first_acc[0])
        )
        return data, track_sentence

generator = MyGenerator()
generator.generate_paradigm(number_to_generate=100, rel_output_path="outputs/inductive_biases/%s.jsonl" % generator.uid)
