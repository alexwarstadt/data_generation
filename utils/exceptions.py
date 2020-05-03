
class LengthHelperError(Exception):
    def __init__(self, sentence, too_long):
        self.sentence = sentence
        self.too_long = too_long


class LexicalGapError(Exception):
    def __init__(self, msg):
        self.msg = msg


class NonUniqueError(Exception):
    def __init__(self, msg):
        self.msg = msg


class MatchNotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg


class FieldAbsentError(Exception):
    def __init__(self, msg):
        self.msg = msg
