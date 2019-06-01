
import csv
from threading import Lock


class UserTweetCounter:
    def __init__(self, user):
        self.user = user
        self.counter = 0

    def increment(self, n):
        self.counter += n

    def same_user(self, user):
        return self.user == user

    def get_user(self):
        return self.user

    def get_counter(self):
        return self.counter

    def __str__(self):
        return 'user: {} - counter {}'.format(self.user, self.counter)

    def print(self):
        print(str(self))

    def report(self):
        result = False
        if self.counter > 3:
            result = True
        return result

    def to_dict(self):
        return {'author_id': self.user, 'negative_tweets': self.counter}


class UsersTweetRecords:

    def __init__(self):
        self.users_tweet_recs = []
        self.lock = Lock()

    def increment(self, user, n=1):
        found = False
        # search for the date
        for ur in self.users_tweet_recs:
            if ur.same_user(user):
                # increment and set found to True
                ur.increment(n)
                found = True
                break

        if not found:
            ur = UserTweetCounter(user)
            ur.increment(n)
            self.users_tweet_recs.append(ur)
        return None

    def print(self):
        for ur in self.users_tweet_recs:
            ur.print()

    def empty(self):
        return len(self.users_tweet_recs)

    def save_to_file(self):
        with open("./results/negative_users_report.txt", 'w') as f:
            for utr in self.users_tweet_recs:
                if utr.report():
                    f.write(str(utr.get_user()) + '\n')
            f.close()

    def flush(self, pipe):
        self.lock.acquire()
        try:
            for utr in self.users_tweet_recs:
                pipe.send(utr.to_dict())
            for utr in self.users_tweet_recs:
                self.users_tweet_recs.remove(utr)
        finally:
            self.lock.release()


class DayTweetCounter:

    def __init__(self, date):
        self.date = date
        self.positive_tweets = 0
        self.negative_tweets = 0

    def increment_negative(self, n):
        self.negative_tweets += n

    def increment_positive(self, n):
        self.positive_tweets += n

    def same_date(self, date):
        return self.date == date

    def __str__(self):
        return 'day: {} - total positives: {} - total negatives: {}'.format(self.date,
                                                                            self.positive_tweets,
                                                                            self.negative_tweets)

    def print(self):
        print(str(self))

    def to_dict(self):
        return {'day': self.date, 'positive_tweets': self.positive_tweets, 'negative_tweets': self.negative_tweets}


class DayTweetRecords:

    def __init__(self):
        self.day_tweet_recs = []
        self.lock = Lock()

    # TODO: remove duplicate code
    def increment_positive(self, date, n=1):
        self.lock.acquire()

        found = False
        # search for the date
        for dr in self.day_tweet_recs:
            if dr.same_date(date):
                # increment and set found to True
                dr.increment_positive(n)
                found = True
                break

        if not found:
            dr = DayTweetCounter(date)
            dr.increment_positive(n)
            self.day_tweet_recs.append(dr)

        self.lock.release()
        return None

    def increment_negative(self, date, n=1):
        self.lock.acquire()

        found = False
        # search for the date
        for dr in self.day_tweet_recs:
            if dr.same_date(date):
                # increment and set found to True
                dr.increment_negative(n)
                found = True
                break

        if not found:
            dr = DayTweetCounter(date)
            dr.increment_negative(n)
            self.day_tweet_recs.append(dr)

        self.lock.release()
        return None

    def print(self):
        for dr in self.day_tweet_recs:
            dr.print()

    def empty(self):
        return len(self.day_tweet_recs)

    def save_to_file(self):
        with open("./results/daily_tweets_report.txt", 'w') as f:
            writer = csv.DictWriter(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                    fieldnames=['day', 'positive_tweets', 'negative_tweets'])
            for dtr in self.day_tweet_recs:
                #f.write(dtr.get_dict())
                #print(str(dtr))
                f.write(str(dtr) + '\n')
            f.close()

    def flush(self, pipe):
        self.lock.acquire()
        try:
            for dtr in self.day_tweet_recs:
                pipe.send(dtr.to_dict())
            for dtr in self.day_tweet_recs:
                self.day_tweet_recs.remove(dtr)

        finally:
            self.lock.release()
