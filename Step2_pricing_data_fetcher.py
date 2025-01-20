import pandas as pd
import requests
import csv
from datetime import datetime

# API details
API_KEY = "6b05e857-65d2-42e5-8196-f23c97a19009"
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
HEADERS = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}

def load_coins_to_track(file_path):
    """Reads the coins_to_track.csv file and returns a DataFrame."""
    return pd.read_csv(file_path)

def fetch_pricing_data(symbols):
    """Fetches pricing data for given symbols from the API."""
    params = {"symbol": ",".join(symbols)}
    response = requests.get(URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
    return response.json()

def save_pricing_data_to_csv(data, output_file):
    """
    Saves the pricing data to a CSV with metadata, excluding
    'percent_change_24h' as per the assignment instructions.
    """
    pricing_data = []
    for symbol, details in data["data"].items():
        pricing_data.append([
            symbol,  # Cryptocurrency symbol
            details["quote"]["USD"]["price"],  # Current price in USD
            details["cmc_rank"],  # Market rank
            datetime.now(),  # Timestamp when the data was loaded
            details["cmc_rank"] <= 10,  # IsTopCurrency
        ])

    # Save to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["symbol", "price", "rank", "LoadedWhen", "IsTopCurrency"])  # Header row
        writer.writerows(pricing_data)

def main():
    # Step 1: Load coins to track
    coins_to_track = load_coins_to_track("coins_to_track.csv")
    symbols = coins_to_track["Symbol"].tolist()

    # Step 2: Fetch pricing data
    data = fetch_pricing_data(symbols)

    # Step 3: Save to timestamped CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"pricing_data_{timestamp}.csv"
    save_pricing_data_to_csv(data, output_file)
    print(f"Pricing data saved to {output_file}")

if __name__ == "__main__":
    main()