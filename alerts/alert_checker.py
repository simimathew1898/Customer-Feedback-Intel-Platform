import pandas as pd
from datetime import datetime, timedelta
import requests

# Load feedback data
df = pd.read_csv("data/feedback_with_sentiment.csv", parse_dates=["timestamp"])

# Set threshold and time window
NEGATIVE_THRESHOLD = 0.30  # 30%
TIME_WINDOW_HOURS = 24

# Filter last 24 hours of feedback
now = datetime.utcnow()
past_24h = df[df['timestamp'] >= (now - timedelta(hours=TIME_WINDOW_HOURS))]

# Calculate negative feedback ratio
if not past_24h.empty:
    total = len(past_24h)
    negative = len(past_24h[past_24h['sentiment'] == 'negative'])
    negative_ratio = negative / total

    # If negative ratio exceeds threshold, send alert
    if negative_ratio > NEGATIVE_THRESHOLD:
        msg = f"Alert: {round(negative_ratio * 100, 2)}% of feedback in the last 24h is negative! ({negative}/{total})"
        print(msg)

        # Send to Slack (Optional)
        webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
        slack_data = {"text": msg}

        try:
            response = requests.post(webhook_url, json=slack_data)
            if response.status_code != 200:
                print("Slack alert failed:", response.text)
            else:
                print("Slack alert sent.")
        except Exception as e:
            print("Error sending Slack alert:", e)

