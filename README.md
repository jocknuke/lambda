
# 📈 Stock Sentiment Analyzer (AWS Lambda)

This AWS Lambda function retrieves recent tweets about a given stock ticker, analyzes the sentiment of each tweet using Amazon Comprehend, and stores the results in a DynamoDB table for further analysis and visualization.

---

## 🛠 Features

- Fetches recent tweets from Twitter/X using the Twitter API v2
- Analyzes sentiment (Positive, Neutral, Negative, Mixed) using AWS Comprehend
- Stores tweet text and sentiment in DynamoDB
- Deployable via AWS Lambda + API Gateway
- Can be integrated with a simple frontend to visualize sentiment trends

---

## 📦 Project Structure

```
stock-sentiment-lambda/
├── lambda_function.py       # Main Lambda function code
├── requirements.txt         # External Python packages (requests)
├── README.md                # This file
├── package/                 # Build directory (created when packaging)
└── stock-sentiment.zip      # Deployment package (to upload to Lambda)
```

---

## ⚙️ Prerequisites

- Python 3.8 or higher
- AWS account with permissions to:
  - Lambda
  - Comprehend
  - DynamoDB
  - Systems Manager (SSM) Parameter Store
- Twitter API Bearer Token

---

## 🔐 AWS Resources Required

1. **DynamoDB Table**: `StockSentiment`  
   - Primary Key: `id` (String)

2. **SSM Parameter**: `/twitter/bearer_token`  
   - Stores your Twitter API bearer token (set `WithDecryption` enabled)

3. **Lambda IAM Role** with permissions:
   - `ssm:GetParameter`
   - `comprehend:DetectSentiment`
   - `dynamodb:PutItem`

---

## 🧪 Sample Event Input (for testing)

```json
{
  "ticker": "TSLA"
}
```

---

## 🐍 Packaging Instructions

```bash
# Create directory
mkdir stock-sentiment-lambda && cd stock-sentiment-lambda

# Create requirements file
echo "requests" > requirements.txt

# Create your lambda_function.py and paste your code

# Install and package
mkdir package
pip install -r requirements.txt -t package/
cp lambda_function.py package/
cd package
zip -r9 ../stock-sentiment.zip .
```

Then upload `stock-sentiment.zip` in the AWS Lambda Console.

---

## 🌐 API Gateway Integration (Optional)

You can expose the Lambda via API Gateway to allow web access.

- Method: `POST`
- Body:
  ```json
  { "ticker": "AAPL" }
  ```

---

## 📊 Frontend Integration (Optional)

You can build a simple HTML + JavaScript frontend using Chart.js to display the sentiment results returned from the Lambda function.

---

## 🧹 TODOs

- Rate limit handling for Twitter API
- Advanced charting with historical trends
- Add SNS or notification integration

---

## 📄 License

MIT License
