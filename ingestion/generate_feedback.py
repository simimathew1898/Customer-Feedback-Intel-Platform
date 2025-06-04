import random
import csv
from datetime import datetime, timedelta
from faker import Faker
import os

fake = Faker()
channels = ['app', 'web', 'survey', 'email']
regions = ['US', 'UK', 'IN', 'AU']
ratings = [1, 2, 3, 4, 5]

messages = {
    1: ["Terrible experience", "App crashed"],
    2: ["Not great", "Slow response"],
    3: ["Okay", "Average"],
    4: ["Good experience", "Nice UI"],
    5: ["Excellent!", "Loved the product"]
}
def generate_feedback(n=1000, filename="data/feedback.csv"):
    os.makedirs("data", exist_ok=True)

    with open(filename, mode="w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'channel', 'region', 'customer_id', 'rating', 'message'])

        for _ in range(n):
            rating = random.choice(ratings)
            writer.writerow([
                (datetime.utcnow() - timedelta(minutes=random.randint(0, 10000))).isoformat(),
                random.choice(channels),
                random.choice(regions),
                fake.uuid4(),  # generates a fake user ID
                rating,
                random.choice(messages[rating])
            ])

if __name__ == "__main__":
    generate_feedback(n=1000)
    print("Feedback data generated: data/feedback.csv")
