from src.data.records import UsersTweetRecords, DayTweetRecords
from datetime import datetime


class UserSink:

    def __init__(self, u_field, aggregate_field):

        self.user_field = u_field
        self.aggregate_field = aggregate_field
        self.user_tweet_records = UsersTweetRecords()

    def process(self, msg):
        self.user_tweet_records.increment(msg[self.user_field], int(msg[self.aggregate_field]))

    def print(self):
        self.user_tweet_records.print()

    def save_to_file(self):
        self.user_tweet_records.save_to_file()


class TotalSink:

    def __init__(self, d_field, aggregate_field_p, aggregate_field_n):

        self.date_field = d_field
        self.aggregate_field_p = aggregate_field_p
        self.aggregate_field_n = aggregate_field_n
        self.day_tweet_records = DayTweetRecords()

    def process(self, msg):

        date = msg[self.date_field],

        self.day_tweet_records.increment_positive(date, int(msg[self.aggregate_field_p]))

        self.day_tweet_records.increment_negative(date, int(msg[self.aggregate_field_n]))

        return None

    def print(self):
        self.day_tweet_records.print()

    def save_to_file(self):
        self.day_tweet_records.save_to_file()
