from collections import Counter


class TweetCounter:
    def __init__(self, date, value):
        self.date = date
        self.counter = value

    def increment(self, n):
        self.counter += n

    def same_date(self, date):
        return self.date == date

    def get_counter(self):
        return self.counter

    def print(self):
        print('date: {} - counter {}'.format(self.date, self.counter))


class UserTweetRecord:

    def __init__(self, u_id, negative_t_limit):
        self.user_id = u_id
        self.negative_tweets_limit = negative_t_limit
        self.negative_tweets_record = []

    def increment_negative_tweet(self, date):
        r = False
        found = False
        # search for the date
        for t in self.negative_tweets_record:
            if t.same_date(date):
                # increment and set found to True
                t.increment(1)
                found = True
                if t.get_counter() == self.negative_tweets_limit:
                    r = True
                break

        if not found:
            t = TweetCounter(date, 1)
            self.negative_tweets_record.append(t)
        return r

    def same_id(self, u_id):
        return self.user_id == u_id

    def print(self):
        print('user: {}'.format(self.user_id))
        for nr in self.negative_tweets_record:
            nr.print()


class UsersTweetRecords:

    def __init__(self, negative_t_limit):
        self.negative_tweets_limit = negative_t_limit
        self.users_tweet_recs = []

    def increment_negative_tweet(self, u_id, date):
        r = False
        found = False
        # search for the date
        for ur in self.users_tweet_recs:
            if ur.same_id(u_id):
                # increment and set found to True
                r = ur.increment_negative_tweet(date)
                found = True
                break

        if not found:
            ur = UserTweetRecord(u_id, self.negative_tweets_limit)
            ur.increment_negative_tweet(date)
            self.users_tweet_recs.append(ur)
        return r

    def print(self):
        for ur in self.users_tweet_recs:
            ur.print()


class TotalTweetRecord:

    def __init__(self):
        self.positive_tweets = 0
        self.negative_tweets = 0

    def increment_negative_tweet(self):
        self.negative_tweets += 1

    def increment_positive_tweet(self):
        self.positive_tweets += 1

    def print(self):
        print('total negatives: {} - total positives: {}'.format(self.positive_tweets, self.negative_tweets))

