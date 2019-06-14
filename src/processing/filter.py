import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.processing.processor import Processor


class Filter(Processor):

    def __init__(self, fields, conditions, remove):
        super().__init__()
        self.fields = fields
        self.conditions = conditions
        self.remove = remove

    def process(self, msg):
        check = True
        res = None

        # if conditions is not empty, check them
        if self.conditions:
            for f, c in zip(self.fields, self.conditions):
                check = check & (bool(msg[f]) == c)

        # if the message is gonna be returned check for removing fields
        if check:
            # remove the fields if necessary
            if self.remove:
                for f in self.fields:
                    del msg[f]

            res = msg
        # print(res)
        return [res]

