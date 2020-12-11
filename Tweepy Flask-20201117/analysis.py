import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np

nltk.download('vader_lexicon')

pointMachine = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(x):
    score = pointMachine.polarity_scores(x)
    return score


def create_my_df():
    my_df = pd.read_json('LeBron.json', orient='records')
    my_df['sentiment'] = my_df['tweet'].apply(lambda x: 'NaN' if pd.isnull(x) else sentiment_analyzer_scores(x))
    my_df['compound'] = my_df['sentiment'].apply(lambda score_dict: score_dict['compound'])
    my_df['compound'] = my_df['sentiment'].apply(lambda score_dict: score_dict['compound'])
    my_df['comp_score'] = my_df['compound'].apply(lambda c: 'positive' if c > 0.05 else ('negative' if c < -0.05 else 'neutral'))
    data = my_df.to_json('templates/results.json')
    open("templates/results.html")
    return my_df