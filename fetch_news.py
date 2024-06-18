import requests
from datetime import datetime, timedelta

def fetch_news(api_key, query, from_date, to_date, sources=None):
    url = f'https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&sortBy=relevancy&language=en&apiKey={api_key}'
    if sources:
        url += f"&sources={sources}"
    print(f"Request URL: {url}")  
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Failed to fetch news: {response.status_code}")
        print(f"Response: {response.json()}") 
        return []

if __name__ == "__main__":
    api_key = ''  # NewsAPI key
    query = 'stock market'
    sources = ','.join([
        'bloomberg',
        'financial-times',
        'cnbc',
        'reuters',
        'the-wall-street-journal',
        'the-new-york-times',
        'forbes',
        'business-insider',
        'marketwatch',
        'the-economist',
        'barrons',
        'fortune',
        'yahoo-finance',
        'abc-news',
        'bbc-news',
        'cnn',
        'fox-news',
        'nbc-news',
        'usa-today',
        'the-washington-post',
        'time',
        'newsweek',
        'the-guardian',
        'the-independent',
        'al-jazeera-english',
        'associated-press',
        'bloomberg',
        'cbc-news',
        'cbs-news',
        'cheddar',
        'daily-mail',
        'financial-post',
        'global-news',
        'national-geographic',
        'national-review',
        'news-com-au',
        'politico',
        'techcrunch',
        'the-globe-and-mail',
        'the-hill',
        'the-huffington-post',
        'the-irish-times',
        'the-telegraph',
        'the-times-of-india',
        'vice-news',
        'wired'
    ])
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    news_articles = fetch_news(api_key, query, yesterday, yesterday, sources)
    for article in news_articles:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}\n")
