import re
import streamlit as st
import logging
# from googleapiclient.discovery import build
# import matplotlib.pyplot as plt
# import seaborn as sns
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# from sklearn.feature_extraction.text import CountVectorizer
# from wordcloud import WordCloud
# from cleantext import clean

from comment_extract import comment_extract
from plot_sentiment_distribution import plot_sentiment_distribution
from comment_analyser import comment_analyser
from time_based_analysis import time_based_analysis
from analyze_and_plot_question_comments import analyze_and_plot_question_comments
from toxicity_and_profanity_detection import toxicity_and_profanity_detection
from sentiment_analysis_on_comments import sentiment_analysis_on_comments
import spacy
from emotion_analysis import emotion_analysis
# import os

# try:
#     # Try loading the model
#     nlp = spacy.load("en_core_web_sm")
# except OSError as e:
#     # If model is missing, download it and load again
#     print(f"Error loading 'en_core_web_sm': {e}")
#     print("Attempting to download the model...")
#     os.system("python -m spacy download en_core_web_sm")
#     nlp = spacy.load("en_core_web_sm")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def clear_page():
    st.session_state.url = ""
    st.session_state.df = None
    st.session_state.likes = None
    st.session_state.views = None
    st.session_state.ratio = None
    st.session_state.api_key = ""  # Clear API key if required
    logger.info("Page cleared. Session state reset.")

# Streamlit UI for input and processing
st.title("YouTube Sentiment Analysis")
logger.info("Application started: YouTube Sentiment Analysis")

# Input for YouTube video URL and API Key
url = st.text_input("Enter the YouTube video URL:", value=st.session_state.get('url', ''))
api_key = 'AIzaSyB4M_HhhFoZX1RyqegIB5BYa0BgL3VvwUw'  # st.text_input("Enter your YouTube API Key:")
logger.debug(f"URL entered: {url}")

# Create two columns for buttons
col1, col2 = st.columns([1, 6])  # Create two columns for buttons
with col1:
    analyze_button = st.button("Analyze")
with col2:
    clear_button = st.button("Clear")

# Results container to update the analysis content
results_container = st.empty()

# Handle "Analyze" button click
if analyze_button:
    if url and api_key:
        logger.info("Analyze button clicked. Starting analysis.")
        try:
            df, likes, views, ratio = comment_extract(url, api_key)
            logger.info("Comments successfully extracted.")
            
            if df is not None:
                st.success("Analysis Complete!")
                logger.info("Displaying video statistics and results.")

                st.subheader("Video Statistics")
                st.write(f"**Views:** {views}")
                st.write(f"**Likes:** {likes}")
                st.write(f"**Like-to-View Ratio:** {ratio:.2f}%")

                st.subheader("Sentiment Analysis")
                plot_sentiment_distribution(df)
                
                st.subheader("Sample Comments with Sentiments")
                st.dataframe(df[['author', 'comment', 'timestamp', 'comment_likes', 'sentiment_score', 'sentiment']].head(10))

                # Perform further analysis
                df = comment_analyser(df)
                logger.info("Comments analyzed.")
                df = time_based_analysis(df)
                logger.info("Time-based analysis completed.")
                df = analyze_and_plot_question_comments(df)
                logger.info("Question comments analyzed.")
                df = toxicity_and_profanity_detection(df)
                logger.info("Toxicity and profanity analysis completed.")
                df = emotion_analysis(df)
                logger.info("Emotional Analysis Completed.")

                st.subheader("Complete Analysis Data")
                # Display the final DataFrame sample
                st.dataframe(df[['author', 'comment', 'timestamp', 'comment_likes', 'sentiment_score', 'sentiment',
                                 'comment_length_chars', 'comment_length_words', 'hour', 'day_of_week', 'is_question','emotion']].head(10))
                
                # Convert DataFrame to CSV
                csv_data = df.to_csv(index=False)
                
                # Provide a download button for the entire DataFrame
                st.download_button(
                    label="Download Complete Data",
                    data=csv_data,
                    file_name="youtube_comments_analysis.csv",
                    mime="text/csv"
                )
                logger.info("Analysis results and data download button displayed.")
            else:
                st.error("Error in extracting comments. Please check the URL and try again.")
                logger.error("Error in extracting comments.")
        
        except Exception as e:
            st.error("An error occurred during analysis. Please try again.")
            logger.exception(f"Exception occurred: {e}")
    else:
        st.error("Please provide a correct YouTube URL.")
        logger.warning("Analyze button clicked without valid URL or API key.")

# Handle "Clear" button click
if clear_button:
    clear_page()  # Clear the input fields and reset the page
    logger.info("Clear button clicked.")
