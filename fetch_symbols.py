import pandas as pd
import requests
import json

def fetch_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    # Fetch the HTML content with SSL verification disabled
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Ensure we notice bad responses

    # Read the HTML content into pandas
    tables = pd.read_html(response.text)
    df = tables[0]
    symbols = df['Symbol'].tolist()
    return symbols

if __name__ == "__main__":
    symbols = fetch_sp500_symbols()
    with open('stocks.json', 'w') as file:
        json.dump(symbols, file)
