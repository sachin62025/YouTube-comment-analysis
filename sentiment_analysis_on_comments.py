from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_analysis_on_comments(df):
    analyzer = SentimentIntensityAnalyzer()

    def classify_sentiment(score):
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        else:
            return "Neutral"
    
    df['sentiment_score'] = df['comment'].apply(lambda comment: analyzer.polarity_scores(comment)['compound'])
    df['sentiment'] = df['sentiment_score'].apply(classify_sentiment)
    return df
