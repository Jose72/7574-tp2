from collections import Counter


class UserTweetCounter:
    def __init__(self, user):
        self. user = user
        self.counter = 0

    def increment(self, n):
        self.counter += n
        self.print()

    def same_user(self, user):
        return self.user == user

    def get_user(self):
        return self.user

    def get_counter(self):
        return self.counter

    def print(self):
        print('user: {} - counter {}'.format(self.user, self.counter))


class UsersTweetRecords:

    def __init__(self):
        self.users_tweet_recs = []

    def increment(self, user):
        found = False
        # search for the date
        for ur in self.users_tweet_recs:
            if ur.same_user(user):
                # increment and set found to True
                ur.increment(1)
                found = True
                break

        if not found:
            ur = UserTweetCounter(user)
            ur.increment(1)
            self.users_tweet_recs.append(ur)
        return None

    def print(self):
        for ur in self.users_tweet_recs:
            ur.print()

    def take(self):
        if len(self.users_tweet_recs) > 0:
            return self.users_tweet_recs.pop()
        return None

    def empty(self):
        return len(self.users_tweet_recs)


class DayTweetCounter:

    def __init__(self, date):
        self.date = date
        self.positive_tweets = 0
        self.negative_tweets = 0

    def increment_negative(self, n):
        self.negative_tweets += n
        self.print()

    def increment_positive(self, n):
        self.positive_tweets += n
        self.print()

    def same_date(self, date):
        return self.date == date

    def print(self):
        print('day: {} - total negatives: {} - total positives: {}'.format(self.date, self.positive_tweets, self.negative_tweets))


class DayTweetRecords:

    def __init__(self):
        self.day_tweet_recs = []

    # TODO: remove duplicate code
    def increment_positive(self, date):
        found = False
        # search for the date
        for dr in self.day_tweet_recs:
            if dr.same_date(date):
                # increment and set found to True
                dr.increment_positive(1)
                found = True
                break

        if not found:
            dr = DayTweetCounter(date)
            dr.increment_positive(1)
            self.day_tweet_recs.append(dr)
        return None

    def increment_negative(self, date):
        found = False
        # search for the date
        for dr in self.day_tweet_recs:
            if dr.same_date(date):
                # increment and set found to True
                dr.increment_negative(1)
                found = True
                break

        if not found:
            dr = DayTweetCounter(date)
            dr.increment_negative(1)
            self.day_tweet_recs.append(dr)
        return None

    def print(self):
        for ur in self.day_tweet_recs:
            ur.print()

    def take(self):
        if len(self.day_tweet_recs) > 0:
            return self.day_tweet_recs.pop()
        return None

    def empty(self):
        return len(self.day_tweet_recs)
