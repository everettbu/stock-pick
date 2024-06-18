import requests
from datetime import datetime, timedelta
import json
import sys

def fetch_stock_news(api_key, stock, from_date, to_date, sources=None):
    query = f'"{stock} stock"'
    url = f'https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&sortBy=relevancy&language=en&apiKey={api_key}'
    if sources:
        url += f"&sources={sources}"
    print(f"Request URL: {url}")  # Debugging print
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")  # Debugging print
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        if not articles:
            print("No articles found for the given query.")
        # Retain only relevant fields
        relevant_articles = [
            {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', '')
            }
            for article in articles
        ]
        return relevant_articles
    else:
        print(f"Failed to fetch news: {response.status_code}")
        print(f"Response: {response.json()}")  # Debugging print
        return []

if __name__ == "__main__":
    api_key = ''  # NewsAPI key
    if len(sys.argv) != 2:
        print("Usage: python 3_get_stock_news.py <stock_symbol>")
        sys.exit(1)
    
    top_stock = sys.argv[1]
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    news_articles = fetch_stock_news(api_key, top_stock, yesterday, yesterday)
    
    if news_articles:
        # Save articles to a file
        with open('top_stock_news.json', 'w') as file:
            json.dump(news_articles, file)

    else:
        print("No relevant news articles found.")
