import spacy
import matplotlib.pyplot as plt
import streamlit as st
from cleantext import clean
import pandas as pd
# import subprocess

def analyze_and_plot_question_comments(dataframe):
    comment_column = 'comment'
    # Load the spaCy English model
    # nlp = spacy.load("en_core_web_sm")

    # try:
    nlp = spacy.load("/home/adminuser/venv/lib/python3.12/site-packages/en_core_web_sm")
    # except OSError:
    #     # Download the model if it is not found
    #     # subprocess.call(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
    #     # nlp = spacy.load("en_core_web_sm")
    #     st.write("spaCy model 'en_core_web_sm' is not found. Please ensure it is downloaded.")
    #     return None

    
    # Function to detect if a comment is a question
    def detect_question_nlp(comment):
        doc = nlp(comment)
        return any([token.tag_ == "WRB" or token.tag_ == "WP" for token in doc])  # WRB or WP tags

    # Apply the function to detect questions
    dataframe['is_question'] = dataframe[comment_column].apply(
        lambda x: detect_question_nlp(str(x)) if pd.notnull(x) else False
    )

    # Filter question comments
    question_comments_df = dataframe[dataframe['is_question']]

    # Calculate totals and percentage
    total_comments = len(dataframe)
    total_questions = len(question_comments_df)
    percentage_questions = (total_questions / total_comments) * 100 if total_comments > 0 else 0

    # Display results in Streamlit
    st.write(f"Total Comments: {total_comments}")
    st.write(f"Total Question Comments: {total_questions}")
    st.write(f"Percentage of Question Comments: {percentage_questions:.2f}%")

    # Plotting Question vs Non-Question Distribution
    total_non_questions = total_comments - total_questions
    labels = ['Questions', 'Non-Questions']
    counts = [total_questions, total_non_questions]
    
    # Plot
    plt.figure(figsize=(8, 5))
    plt.bar(labels, counts, color=['skyblue', 'orange'], alpha=0.8)
    plt.title('Distribution of Question vs. Non-Question Comments', fontsize=14)
    plt.ylabel('Number of Comments', fontsize=12)
    plt.xlabel('Comment Type', fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Annotate counts on bars
    for i, count in enumerate(counts):
        plt.text(i, count + 2, str(count), ha='center', fontsize=11)

    st.pyplot(plt)

    return dataframe  
