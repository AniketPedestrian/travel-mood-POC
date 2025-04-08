import tweepy
import os
from dotenv import load_dotenv
import json

load_dotenv()

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
client = tweepy.Client(bearer_token=bearer_token)

# Search query
query = '(lost baggage OR lost luggage OR delayed flight OR travel issue) lang:en -is:retweet'

# Request max tweets (100 limit for free tier)
response = client.search_recent_tweets(
    query=query,
    max_results=100,
    tweet_fields=['created_at', 'geo', 'text', 'author_id']
)

tweets_data = []

# Only collect tweets with geo info
if response.data:
    for tweet in response.data:
        if tweet.geo:
            tweet_info = {
                'id': tweet.id,
                'author_id': tweet.author_id,
                'created_at': tweet.created_at.isoformat(),
                'text': tweet.text,
                'geo': tweet.geo
            }
            tweets_data.append(tweet_info)
            if len(tweets_data) >= 40:
                break

# Save results
with open('tweets.json', 'w') as f:
    json.dump(tweets_data, f, indent=2)

print(f"Saved {len(tweets_data)} tweets with geo info to tweets.json")
