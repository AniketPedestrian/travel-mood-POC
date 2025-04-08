import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


openai = OpenAI(api_key=os.getenv("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"))

with open('tweets.json', 'r') as f:
    tweets = json.load(f)

analyzed_tweets = []

def analyze_tweet(tweet_text):
    prompt = f"""Analyze the sentiment of the tweet as positive, negative, or neutral, and identify the likely location (city/country) mentioned or implied. If no location is implied, respond with 'Not Mentioned'.

Tweet: "{tweet_text}"

Respond in JSON format:
{{
    "sentiment": "",
    "location": ""
}}
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        analysis = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        analysis = {"sentiment": "unknown", "location": "Not Mentioned"}

    return analysis

for tweet in tweets:
    analysis = analyze_tweet(tweet['text'])
    tweet.update(analysis)
    analyzed_tweets.append(tweet)
    print(f"Analyzed tweet: {tweet['id']} | Sentiment: {analysis['sentiment']} | Location: {analysis['location']}")

with open('tweets_analyzed.json', 'w') as f:
    json.dump(analyzed_tweets, f, indent=2)
