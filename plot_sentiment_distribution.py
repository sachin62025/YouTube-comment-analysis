import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Function to plot sentiment distribution
def plot_sentiment_distribution(df):
    sentiment_counts = df['sentiment'].value_counts(normalize=True) * 100

    fig, ax = plt.subplots(figsize=(8, 6))

    # Explicitly setting hue=None and using the palette for x variable
    sns.barplot(
        x=sentiment_counts.index, 
        y=sentiment_counts.values, 
        palette="viridis", 
        ax=ax, 
        hue=None  # Ensures palette is applied without confusion
    )
    
    ax.set_title('Sentiment Distribution of YouTube Comments')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Percentage (%)')
    st.pyplot(fig)
