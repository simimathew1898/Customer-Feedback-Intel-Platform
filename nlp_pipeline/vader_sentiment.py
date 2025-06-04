import csv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create the output folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Input and output file paths
input_file = "data/feedback.csv"
output_file = "data/feedback_with_sentiment.csv"

def classify_sentiment(compound_score):
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"

# Process the file
with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['compound_score', 'sentiment']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for row in reader:
        message = row['message']
        scores = analyzer.polarity_scores(message)
        compound = scores['compound']
        sentiment = classify_sentiment(compound)
        
        row['compound_score'] = round(compound, 4)
        row['sentiment'] = sentiment
        
        writer.writerow(row)

print("Sentiment analysis complete. Output saved to: data/feedback_with_sentiment.csv")
