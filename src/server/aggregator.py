from src.data.records import UsersTweetRecords, DayTweetRecords
from datetime import datetime

class UserAggregator:

    def __init__(self, u_field, aggregate_field, validator):

        self.user_field = u_field
        self.aggregate_field = aggregate_field
        self.condition_validator = validator
        self.user_tweet_records = UsersTweetRecords()

    def process(self, msg):
        ok_to_aggregate = True
        if self.condition_validator:
            ok_to_aggregate = self.condition_validator.validate(msg[self.aggregate_field])

        if ok_to_aggregate:
            self.user_tweet_records.increment(msg[self.user_field])

    def create_messages(self):
        msgs = []
        while not self.user_tweet_records.empty():
            msgs.append(self.user_tweet_records.take())
        return msgs


class TotalAggregator:

    def __init__(self, d_field, aggregate_field, p_validator, n_validator):

        self.date_field = d_field
        self.aggregate_field = aggregate_field
        self.p_validator = p_validator
        self.n_validator = n_validator
        self.day_tweet_records = DayTweetRecords()

    def process(self, msg):
        datetime_object = datetime.strptime(msg[self.date_field], '%a %b %d %H:%M:%S %z %Y')
        date = datetime_object.strftime('%Y-%m-%d')
        score = msg[self.aggregate_field]
        if self.p_validator.validate(score):
            self.day_tweet_records.increment_positive(date)
        else:
            if self.n_validator.validate(score):
                self.day_tweet_records.increment_negative(date)
        return None


class NegativeTweetValidator:

    @staticmethod
    def validate(score):
        result = False
        if int(score) < -0.5:
            result = True
        #print(str(score) + str(result))
        return result


class PositiveTweetValidator:
    @staticmethod
    def validate(score):
        result = False
        if int(score) > 0.5:
            result = True
        # print(str(score) + str(result))
        return result
