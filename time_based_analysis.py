import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


def time_based_analysis(df):
    # Ensure 'timestamp' is in datetime format
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # Extract hour and day of the week
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.day_name()

        # Plot: Comment distribution by hour of the day
        st.subheader("Comment Distribution by Hour of the Day")
        hour_counts = df['hour'].value_counts().sort_index()
        if not hour_counts.empty:
            plt.figure(figsize=(8, 6))
            hour_counts.plot(kind='bar', color='lightblue')
            plt.title('Comment Distribution by Hour of the Day')
            plt.xlabel('Hour of the Day')
            plt.ylabel('Number of Comments')
            st.pyplot(plt)
        else:
            st.warning("No valid timestamps found to analyze hourly distribution.")

        # Plot: Comment distribution by day of the week
        st.subheader("Comment Distribution by Day of the Week")
        day_counts = df['day_of_week'].value_counts()
        if not day_counts.empty:
            ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            plt.figure(figsize=(8, 6))
            day_counts.reindex(ordered_days).plot(kind='bar', color='lightgreen')
            plt.title('Comment Distribution by Day of the Week')
            plt.xlabel('Day of the Week')
            plt.ylabel('Number of Comments')
            st.pyplot(plt)
        else:
            st.warning("No valid timestamps found to analyze day-of-week distribution.")
    else:
        st.error("The DataFrame does not contain a 'timestamp' column.")
    
    # Return the modified DataFrame
    return df


