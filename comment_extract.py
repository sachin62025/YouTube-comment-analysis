import re
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from googleapiclient.discovery import build
# Function to plot sentiment distribution
def plot_sentiment_distribution(df):
    sentiment_counts = df['sentiment'].value_counts(normalize=True) * 100
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis", ax=ax)
    ax.set_title('Sentiment Distribution of YouTube Comments')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Percentage (%)')
    st.pyplot(fig)

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






# Function to extract comments from YouTube
def comment_extract(url, api_key):
    
    def extract_video_id(url):
        # Check for short URL format (youtu.be)
        short_url_pattern = r"youtu\.be/([a-zA-Z0-9_-]+)"
        match = re.search(short_url_pattern, url)
        
        if match:
            return match.group(1)
        
        # Check for full URL format (youtube.com)
        long_url_pattern = r"youtube\.com/watch\?v=([a-zA-Z0-9_-]+)"
        match = re.search(long_url_pattern, url)
        
        if match:
            return match.group(1)
        
        return None

    # Extract video ID
    video_id = extract_video_id(url)

    # pattern = r"v=([a-zA-Z0-9_-]+)"
    # match = re.search(pattern, url)
    
    # if match:
    #     video_id = match.group(1)
    # else:
    #     st.error("Invalid YouTube URL. Please try again.")
    #     return None, None, None, None


    if not video_id:
        st.error("Invalid YouTube URL. Please try again.")
        return None, None, None, None
    
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments_data = []
    
    try:
        # Fetch video statistics
        video_request = youtube.videos().list(part="statistics", id=video_id)
        video_response = video_request.execute()
        
        views = video_response['items'][0]['statistics'].get('viewCount', 0)
        likes = video_response['items'][0]['statistics'].get('likeCount', 0)
        ratio = (int(likes) / int(views)) * 100 if int(views) > 0 else 0
        
        # Fetch comments
        comment_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100
        )
        comment_response = comment_request.execute()
        
        for item in comment_response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            like_count = item["snippet"]["topLevelComment"]["snippet"].get("likeCount", 0)
            timestamp = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            comments_data.append({
                'author': author,
                'comment': comment,
                'comment_likes': like_count,
                'timestamp': timestamp
            })
        
        df = pd.DataFrame(comments_data)
        if df.empty:
            st.warning("No comments found for this video.")
            return None, None, None, None
        
        df = sentiment_analysis_on_comments(df)
        # df = comment_analyser(df)
        return df, likes, views, ratio
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None, None, None









