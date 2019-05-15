

class Aggregator:

    def __init__(self, field, validator):

        self.field = field
        self.condition_validator = validator
        self.counter = []

    def aggregate(self, msg):
        ok_to_aggregate = True
        if self.condition_validator:
            ok_to_aggregate = self.condition_validator.validate(msg[self.field])

        if ok_to_aggregate:
            for c in self.counter:
                if c[0] == msg[self.field]:
                    c[1] += 1



