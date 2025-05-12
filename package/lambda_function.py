import boto3
import uuid
import json
import requests
from datetime import datetime
from collections import Counter

ssm = boto3.client('ssm')
comprehend = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StockSentiment')

def get_bearer_token():
    response = ssm.get_parameter(
        Name='/twitter/bearer_token',
        WithDecryption=True
    )
    return response['Parameter']['Value']

def fetch_tweets(ticker):
    bearer_token = get_bearer_token()
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    query = f'"{ticker}" OR "${ticker}" stock -is:retweet lang:en'
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10"

    response = requests.get(url, headers=headers)
    print("Twitter API URL:", url)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    if response.status_code != 200:
        return []

    tweets = response.json().get("data", [])
    return [tweet["text"] for tweet in tweets]



def lambda_handler(event, context):
    ticker = event.get("ticker", "TSLA")
    tweets = fetch_tweets(ticker)
    sentiment_counts = Counter()

    for tweet in tweets:
        sentiment_response = comprehend.detect_sentiment(Text=tweet, LanguageCode='en')
        sentiment = sentiment_response['Sentiment']
        sentiment_counts[sentiment] += 1

        table.put_item(Item={
            'id': str(uuid.uuid4()),
            'Ticker': ticker,
            'Text': tweet,
            'Sentiment': sentiment,
            'Timestamp': datetime.utcnow().isoformat()
        })

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'ticker': ticker,
            'count': len(tweets),
            'sentimentSummary': dict(sentiment_counts)
        })
    }