import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
import streamlit as st

emotion_model = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")

def emotion_analysis(df):
    emotions = []
    for comment in df['comment']:
        emotion = emotion_model(comment)
        # Append the emotion label to the emotions list
        emotions.append(emotion[0]['label'])
    df['emotion'] = emotions
    
    emotion_counts = df['emotion'].value_counts()
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 5))
    emotion_counts.plot(kind='bar', color=['#ff9999','#66b3ff','#99ff99','#ffcc99', '#f1c40f'], edgecolor='black', ax=ax)
    ax.set_title("Emotion Distribution in Comments", fontsize=16)
    ax.set_xlabel("Emotion", fontsize=12)
    ax.set_ylabel("Number of Comments", fontsize=12)
    ax.set_xticklabels(emotion_counts.index, rotation=45, fontsize=10)
    
    # Display the plot using Streamlit
    st.pyplot(fig)
    st.subheader("Top 5 Comments for Each Emotion")
    # Loop through all unique emotions and display top 5 comments for each emotion
    for emotion in emotion_counts.index:
        st.write(f"### {emotion} Emotion:")
        # Get the top 5 comments for the current emotion
        top_comments = df[df['emotion'] == emotion].nlargest(5, 'comment_likes')[['comment', 'author', 'comment_likes']]
        st.dataframe(top_comments)
    return df

