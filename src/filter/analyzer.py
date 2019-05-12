import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class TweetAnalyzer:

    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    # return 1 if its a positive tweet
    # 0 if no
    def analyze(self, text):
        score = self.sentiment_analyzer.polarity_scores(text)['compound']
        r = 1
        if score < 0:
            r = 0
        return r
