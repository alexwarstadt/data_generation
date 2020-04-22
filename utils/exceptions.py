
class LengthHelperError(Exception):
    def __init__(self, sentence, too_long):
        self.sentence = sentence
        self.too_long = too_long

