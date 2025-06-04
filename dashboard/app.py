import pandas as pd
import streamlit as st
from datetime import datetime

# Load and preprocess data
df = pd.read_csv("data/feedback_with_sentiment.csv", parse_dates=["timestamp"])

st.set_page_config(page_title="Customer Feedback Dashboard", layout="wide")

# Page title
st.title("Customer Feedback Intelligence Platform")
st.markdown("Analyze sentiment trends across customer feedback in real time.")

# --- Sidebar Filters ---
st.sidebar.header("Filter Feedback")

# Date range
min_date = df['timestamp'].min().date()
max_date = df['timestamp'].max().date()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])
df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

# Region
regions = ["All"] + sorted(df['region'].unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)
if selected_region != "All":
    df = df[df['region'] == selected_region]

# Channel
channels = ["All"] + sorted(df['channel'].unique().tolist())
selected_channel = st.sidebar.selectbox("Channel", channels)
if selected_channel != "All":
    df = df[df['channel'] == selected_channel]

# Sentiment
sentiments = ["All"] + ["positive", "neutral", "negative"]
selected_sentiment = st.sidebar.selectbox("Sentiment", sentiments)
if selected_sentiment != "All":
    df = df[df['sentiment'] == selected_sentiment]

# --- Metrics ---
st.subheader("Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Feedback", len(df))
col2.metric("Avg. Rating", round(df['rating'].mean(), 2))
col3.metric("Negative Feedback %", f"{round((df['sentiment'] == 'negative').mean() * 100, 2)}%")

# --- Visualizations ---
with st.expander("Sentiment Distribution", expanded=True):
    st.bar_chart(df['sentiment'].value_counts())

with st.expander("⭐ Rating Distribution", expanded=True):
    st.bar_chart(df['rating'].value_counts().sort_index())

# --- Table ---
st.subheader("Filtered Feedback Messages")
st.dataframe(df[['timestamp', 'channel', 'region', 'rating', 'sentiment', 'message']])
