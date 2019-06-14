from datetime import datetime
from src.data.records import UsersTweetRecords, DayTweetRecords
from src.processing.processor import Processor



class UserAggregator(Processor):

    def __init__(self, u_field, aggregate_field, validator):

        super().__init__()
        self.user_field = u_field
        self.aggregate_field = aggregate_field
        self.condition_validator = validator
        self.user_tweet_records = UsersTweetRecords()
        self.time = datetime.now()

    def process(self, msg):
        ok_to_aggregate = True
        if self.condition_validator:
            ok_to_aggregate = self.condition_validator.validate(msg[self.aggregate_field])

        if ok_to_aggregate:
            self.user_tweet_records.increment(msg[self.user_field])

        # if 10 sec passed between the last call, flush the data
        if (self.time - datetime.now()).total_seconds() > 10:
            self.time = datetime.now()
            return self.flush()

        return []

    def print(self):
        self.user_tweet_records.print()

    def save_to_file(self):
        self.user_tweet_records.save_to_file()

    def flush(self):
        return self.user_tweet_records.flush()

class TotalAggregator(Processor):

    def __init__(self, d_field, aggregate_field):
        super().__init__()
        self.date_field = d_field
        self.aggregate_field = aggregate_field
        self.day_tweet_records = DayTweetRecords()
        self.time = datetime.now()

    def process(self, msg):
        datetime_object = datetime.strptime(msg[self.date_field], '%a %b %d %H:%M:%S %z %Y')
        date = datetime_object.strftime('%Y-%m-%d')
        score = msg[self.aggregate_field]

        # increment
        if int(score) == 1:
            self.day_tweet_records.increment_positive(date)
        else:
            if int(score) == -1:
                self.day_tweet_records.increment_negative(date)

        # if 10 sec passed between the last call, flush the data
        if (self.time - datetime.now()).total_seconds() > 10:
            self.time = datetime.now()
            return self.flush()

        return []

    def print(self):
        self.day_tweet_records.print()

    def save_to_file(self):
        self.day_tweet_records.save_to_file()

    def flush(self):
        return self.day_tweet_records.flush()


class NegativeTweetValidator:

    @staticmethod
    def validate(score):
        result = False
        if int(score) < -0.5:
            result = True
        return result


class PositiveTweetValidator:
    @staticmethod
    def validate(score):
        result = False
        if int(score) > 0.5:
            result = True
        return result
