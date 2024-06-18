import openai
import json

def estimate_token_count(text):
    return len(text.split())

def format_article(article):
    title = article.get('title', 'No title')
    description = article.get('description', 'No description')
    url = article.get('url', 'No URL')
    return f"Title: {title}\nDescription: {description}\nURL: {url}\n\n"

def generate_prompt(stock, articles, max_tokens):
    prompt_base = f"Generate an article about the following stock: {stock} using information provided in the articles. You are to be informative and have positive sentiment.:\n\n"
    current_tokens = estimate_token_count(prompt_base)
    prompt = prompt_base

    for article in articles:
        article_text = format_article(article)
        article_tokens = estimate_token_count(article_text)

        if current_tokens + article_tokens < max_tokens - 500:
            prompt += article_text
            current_tokens += article_tokens
        else:
            break

    return prompt

def generate_summary(api_key, stock, articles):
    openai.api_key = api_key
    max_tokens = 8192
    prompt = generate_prompt(stock, articles, max_tokens)

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    return response['choices'][0]['message']['content'].strip()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_summary(summary):
    with open(f'summary.txt', 'w') as file:
        file.write(summary)

if __name__ == "__main__":
    api_key = '' # OpenAI API
    top_stock_data = load_json('top_stock.json')
    top_stock = top_stock_data['top_stock']
    top_stock_articles = load_json('top_stock_news.json')

    summary = generate_summary(api_key, top_stock, top_stock_articles)

    save_summary(top_stock, summary)
