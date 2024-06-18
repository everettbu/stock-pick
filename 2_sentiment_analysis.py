from transformers import pipeline
import json
from collections import defaultdict
import subprocess

def analyze_sentiment(articles):
    sentiment_pipeline = pipeline('sentiment-analysis')
    sentiments = []
    for article in articles:
        if article['description']:
            sentiment = sentiment_pipeline(article['description'][:512])  # Truncate to the first 512 characters for efficiency
            sentiments.append((article['title'], article['description'], sentiment[0]))
    return sentiments

def extract_stock_mentions(articles, stock_symbols):
    stock_mentions = defaultdict(int)
    stock_sentiments = defaultdict(list)

    for title, description, sentiment in articles:
        positive_sentiment = sentiment['label'] == 'POSITIVE'
        for stock in stock_symbols:
            if stock in title or stock in description:
                if positive_sentiment:
                    stock_mentions[stock] += 1
                    stock_sentiments[stock].append(sentiment['score'])
    
    return stock_mentions, stock_sentiments

def select_top_stock(stock_mentions, stock_sentiments, mention_weight=0.5, score_weight=0.5):
    top_stock = None
    highest_combined_score = 0

    for stock, mentions in stock_mentions.items():
        if stock_sentiments[stock]:  # Ensure there are positive sentiments
            average_sentiment = sum(stock_sentiments[stock]) / len(stock_sentiments[stock])
            combined_score = (mentions * mention_weight) + (average_sentiment * score_weight)
            if combined_score > highest_combined_score:
                highest_combined_score = combined_score
                top_stock = stock

    return top_stock, highest_combined_score

if __name__ == "__main__":
    # Read articles from file
    with open('news_articles.json', 'r') as file:
        articles = json.load(file)

    # Read stock symbols from file
    with open('stocks.json', 'r') as file:
        stock_symbols = json.load(file)

    sentiments = analyze_sentiment(articles)
    stock_mentions, stock_sentiments = extract_stock_mentions(sentiments, stock_symbols)
    top_stock, highest_combined_score = select_top_stock(stock_mentions, stock_sentiments)

    if top_stock:
        print(f"Top stock: {top_stock} with a combined score of {highest_combined_score}")
        
        # Save the top stock symbol to a file
        with open('top_stock.json', 'w') as file:
            json.dump({"top_stock": top_stock}, file)

        # Fetch articles for the top stock from the previous day
        subprocess.run(["python", "3_get_stock_news.py", top_stock])

    else:
        print("No top stock found with positive sentiment.")
