import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src.processing.processor import Processor
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class TextProcessor(Processor):

    def __init__(self, field, new_field, remove):
        super().__init__()
        self.analyzer = TextAnalyzer()
        self.field = field
        self.new_field = new_field
        self.remove = remove

    def process(self, msg):
        text = msg[self.field]
        score = self.analyzer.analyze(text)
        msg.update({self.new_field: score})
        if self.remove:
            del msg[self.field]
        # print(msg)

        return [msg]


class TextAnalyzer:

    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    # return 1 if its a positive tweet
    # -1 if negative, 0 otherwise
    def analyze(self, text):
        score = self.sentiment_analyzer.polarity_scores(text)['compound']
        r = 0
        if score < -0.5:
            r = -1
        if score > 0.5:
            r = 1
        return r
