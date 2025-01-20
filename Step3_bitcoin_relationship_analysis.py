import pandas as pd
import requests
from datetime import datetime

# API details
API_KEY = "6b05e857-65d2-42e5-8196-f23c97a19009"
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
HEADERS = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}


def fetch_percent_change_24h(symbols):
    """
    Fetches the 24-hour percent change for the given symbols from the API.

    Args:
        symbols (list): List of cryptocurrency symbols to fetch data for.

    Returns:
        dict: A dictionary where the keys are symbols and the values are 24-hour percent changes.
    """
    params = {"symbol": ",".join(symbols)}
    response = requests.get(URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

    data = response.json()["data"]
    percent_changes = {symbol: data[symbol]["quote"]["USD"]["percent_change_24h"] for symbol in data}
    return percent_changes


def analyze_relationship_with_bitcoin(input_file, output_file):
    """
    Analyzes the relationship between Bitcoin and other cryptocurrencies
    by calculating the absolute difference in their 24-hour percent changes.

    Args:
        input_file (str): Path to the pricing data CSV file.
        output_file (str): Path to the output CSV file.
    """
    # Step 1: Load the pricing data
    data = pd.read_csv(input_file)

    # Step 2: Fetch 24-hour percent change data from the API
    symbols = data["symbol"].tolist()
    percent_changes = fetch_percent_change_24h(symbols)

    # Step 3: Extract Bitcoin's 24-hour percent change
    bitcoin_percent_change = percent_changes.get("BTC")
    if bitcoin_percent_change is None:
        raise ValueError("Bitcoin (BTC) data is not available in the API response.")

    # Step 4: Calculate the absolute difference for each cryptocurrency
    data["percent_change_24h"] = data["symbol"].map(percent_changes)
    data["Difference"] = abs(data["percent_change_24h"] - bitcoin_percent_change)

    # Step 5: Sort the data by the Difference column
    data_sorted = data.sort_values(by="Difference")

    # Step 6: Save the sorted data to a new CSV file
    data_sorted.to_csv(output_file, index=False)
    print(f"Relationship analysis saved to {output_file}")


def main():
    # Example file paths (update these if necessary)
    # Here remember to replace the name of the actual file that was produced with the latest timestamp
    input_file = "pricing_data_20250116_175352.csv"  # Replace with actual file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"btc_relationship_{timestamp}.csv"

    # Perform the analysis
    analyze_relationship_with_bitcoin(input_file, output_file)


if __name__ == "__main__":
    main()