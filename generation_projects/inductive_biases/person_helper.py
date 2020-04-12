from utils import data_generator
from utils.constituent_building import *
from utils.conjugate import *
from utils.randomize import choice
import random

class PersonGenerator(data_generator.InductiveBiasesGenerator):
    def __init__(self,
                 uid: str,
                 linguistic_feature_type: str,
                 linguistic_feature_description: str,
                 surface_feature_type: str,
                 surface_feature_description: str,
                 control_paradigm: bool):
        super().__init__(uid,
                         linguistic_feature_type,
                         linguistic_feature_description,
                         surface_feature_type,
                         surface_feature_description,
                         control_paradigm)

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
        # self.safe_animate_common_nouns = np.setdiff1d(np.intersect1d(all_common_nouns, all_animate_nouns), get_all("expression", "doctor"))

    def get_pronouns(self):
        r = random.random()     # randomly select either a nominative pronoun, possessive determiner, or possessive pronoun
        if r < 1/3:  # nominative pronoun
            first = choice(np.intersect1d(self.first, self.nom_pronoun))
            non_first = choice(np.setdiff1d(self.nom_pronoun, self.first))
            first_acc = choice(get_all_conjunctive([("person", first["person"]), ("sg", first["sg"])], self.acc_pronoun))
            non_first_acc = choice(get_all_conjunctive([("person", non_first["person"]), ("sg", non_first["sg"])], self.acc_pronoun))
        elif r < 2/3:   # possessive det
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
        return first, non_first, first_acc, non_first_acc