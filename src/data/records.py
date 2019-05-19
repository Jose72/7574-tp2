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

