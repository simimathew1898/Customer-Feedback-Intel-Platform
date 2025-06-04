import pandas as pd
import streamlit as st

# Load the dataset
df = pd.read_csv("data/feedback_with_sentiment.csv")

# App title
st.title("Customer Feedback Intelligence Dashboard")

# Show metrics
st.subheader("Overall Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Feedback", len(df))
col2.metric("Avg. Rating", round(df['rating'].mean(), 2))
col3.metric("Positive Feedback", sum(df['sentiment'] == "positive"))

# Sentiment distribution
st.subheader("Sentiment Breakdown")
sentiment_counts = df['sentiment'].value_counts()
st.bar_chart(sentiment_counts)

# Rating distribution
st.subheader("Rating Distribution")
rating_counts = df['rating'].value_counts().sort_index()
st.bar_chart(rating_counts)

# Region filter
st.subheader("Feedback by Region")
selected_region = st.selectbox("Choose a region", ["All"] + sorted(df['region'].unique().tolist()))
if selected_region != "All":
    df = df[df['region'] == selected_region]
    st.write(f"Showing feedback for **{selected_region}** only.")

# Show sample data
st.dataframe(df[['timestamp', 'channel', 'region', 'rating', 'sentiment', 'message']])
