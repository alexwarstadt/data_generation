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
        self.third = get_all("person", "3")
        self.safe_verbs = get_all("ing", "0", all_verbs)   # This is because auxiliaries "be" and "have" for 1st and 2nd person not implemented
        self.cp_verb = get_all("category", "(S\\NP)/S", self.safe_verbs)
        self.trans_verb = np.intersect1d(self.safe_verbs, all_anim_anim_verbs)
        self.dets = get_all("category_2", "D")
        self.possessible_animates = get_all("category", "N\\NP[poss]")
        # self.safe_animate_common_nouns = np.setdiff1d(np.intersect1d(all_common_nouns, all_animate_nouns), get_all("expression", "doctor"))

    def get_pronouns(self):
        r = random.random()     # randomly select either a nominative pronoun, possessive determiner, or possessive pronoun
        if r < 1/3:  # nominative pronoun
            third = choice(np.intersect1d(self.third, self.nom_pronoun))
            non_third = choice(np.setdiff1d(self.nom_pronoun, self.third))
            third_acc = choice(get_all_conjunctive([("person", third["person"]), ("sg", third["sg"])], self.acc_pronoun))
            non_third_acc = choice(get_all_conjunctive([("person", non_third["person"]), ("sg", non_third["sg"])], self.acc_pronoun))
        elif r < 2/3:   # possessive det
            noun = choice(self.possessible_animates)
            third_det = choice(get_all("person", "3", self.poss_det))
            third = noun.copy()
            third[0] = third_det[0] + " " + third[0]
            non_third_det = choice(np.setdiff1d(self.poss_det, self.third))
            non_third = noun.copy()
            non_third[0] = non_third_det[0] + " " + non_third[0]
            third_acc = choice(get_all_conjunctive([("person", third_det["person"]), ("sg", third_det["sg"])], self.acc_pronoun))
            non_third_acc = choice(get_all_conjunctive([("person", non_third_det["person"]), ("sg", non_third_det["sg"])], self.acc_pronoun))
        else:   # possessive pronoun
            third = choice(get_all("person", "3", self.poss_pronoun))
            non_third = choice(np.setdiff1d(self.poss_pronoun, self.third))
            third_acc = choice(get_all_conjunctive([("person", third["person"]), ("sg", third["sg"])], self.acc_pronoun))
            non_third_acc = choice(get_all_conjunctive([("person", non_third["person"]), ("sg", non_third["sg"])], self.acc_pronoun))
            vals = ["1", "0"]
            sg = random.choice(["1", "0"])  # Possessive pronouns can have either singular or plural agreement, irrespective of person/number marking
            vals.remove(sg)
            pl = vals[0]
            third["sg"] = sg
            third["pl"] = pl
            non_third["sg"] = sg
            non_third["pl"] = pl
        return third, non_third, third_acc, non_third_acc