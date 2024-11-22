import streamlit as st
from cleantext import clean

def toxicity_and_profanity_detection(df):
    # Clean the 'comment' column to remove unwanted characters
    df['clean_comment'] = df['comment'].apply(lambda x: clean(x))
    
    # List of simple toxic keywords (could be expanded or replaced with a model)
    toxic_keywords = ['hate', 'angry', 'stupid', 'idiot', 'bad']
    
    # Identify toxic comments by searching for toxic keywords
    df['is_toxic'] = df['comment'].apply(lambda x: any(word in x.lower() for word in toxic_keywords))
    
    # Calculate and display the percentage of toxic comments
    toxic_percentage = df['is_toxic'].mean() * 100
    st.subheader(f"Percentage of Toxic Comments: {toxic_percentage:.2f}%")
    
    toxic_comments = df[df['is_toxic']]
    if not toxic_comments.empty:
        st.subheader("Toxic Comments")
        st.write(toxic_comments[['author', 'comment']])
    else:
        st.info("No toxic comments detected.")

    return df
