import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Function to generate word cloud
def generate_wordcloud(df):
    all_comments = ' '.join(df['comment'].tolist())
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_comments)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

# Function for n-gram analysis
def n_gram_analysis(df, n=2):
    vectorizer = CountVectorizer(ngram_range=(n, n), stop_words='english')
    ngram_matrix = vectorizer.fit_transform(df['comment'])
    ngrams = vectorizer.get_feature_names_out()
    sum_ngrams = ngram_matrix.sum(axis=0).A1
    ngram_freq = dict(zip(ngrams, sum_ngrams))
    sorted_ngrams = sorted(ngram_freq.items(), key=lambda item: item[1], reverse=True)
    return sorted_ngrams[:10]


# Function for comment analysis
def comment_analyser(df):
    st.subheader("Word Cloud")
    generate_wordcloud(df)

    st.subheader("N-Gram Analysis (Bigrams)")
    ngrams = n_gram_analysis(df, n=2)
    st.write("Most Common Bigrams:")
    for ngram, freq in ngrams:
        st.write(f"{ngram}: {freq}")

    st.subheader("Comment Length Analysis")
    df['comment_length_chars'] = df['comment'].apply(len)
    df['comment_length_words'] = df['comment'].apply(lambda x: len(x.split()))

    # Plot histograms
    st.write("Length Distribution (Characters):")
    fig, ax = plt.subplots(figsize=(8, 6))
    df['comment_length_chars'].plot(kind='hist', bins=30, color='skyblue', edgecolor='black', ax=ax)
    plt.title('Comment Length Distribution (Characters)')
    plt.xlabel('Length (characters)')
    plt.ylabel('Frequency')
    st.pyplot(fig)

    st.write("Length Distribution (Words):")
    fig, ax = plt.subplots(figsize=(8, 6))
    df['comment_length_words'].plot(kind='hist', bins=30, color='lightgreen', edgecolor='black', ax=ax)
    plt.title('Comment Length Distribution (Words)')
    plt.xlabel('Length (words)')
    plt.ylabel('Frequency')
    st.pyplot(fig)

    # Correlation
    correlation_chars_sentiment = df['comment_length_chars'].corr(df['sentiment_score'])
    correlation_words_sentiment = df['comment_length_words'].corr(df['sentiment_score'])
    st.write(f"Correlation between comment length (characters) and sentiment: {correlation_chars_sentiment}")
    st.write(f"Correlation between comment length (words) and sentiment: {correlation_words_sentiment}")

    st.subheader("Top Liked Comments")
    top_liked_comments = df[['author', 'comment', 'comment_likes']].sort_values(by='comment_likes', ascending=False).head(10)
    st.dataframe(top_liked_comments)

    st.subheader("Likes Distribution")
    fig, ax = plt.subplots(figsize=(8, 6))
    df['comment_likes'].plot(kind='hist', bins=30, color='salmon', edgecolor='black', ax=ax)
    plt.title('Likes Distribution on Comments')
    plt.xlabel('Number of Likes')
    plt.ylabel('Frequency')
    st.pyplot(fig)

    st.subheader("Top Commenters")
    top_commenters = df['author'].value_counts().head(10)
    st.write(top_commenters)

    # st.subheader("Average Sentiment of Top Commenters")
    # top_commenter_data = df[df['author'].isin(top_commenters.index)]
    # top_commenter_sentiment = top_commenter_data.groupby('author')['sentiment_score'].mean()
    # st.write(top_commenter_sentiment)
    return df