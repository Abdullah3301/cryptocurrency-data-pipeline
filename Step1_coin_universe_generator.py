import requests
## We perfrom this step to check if the API Key returns us any values or not before we proceed further

# Define API details
api_key = '6b05e857-65d2-42e5-8196-f23c97a19009'
base_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

# Set headers for the API request
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

# Make a GET request to the API
response = requests.get(base_url, headers=headers)

# Check response
if response.status_code == 200:
    data = response.json()
    print("API Test Successful! Here is a sample of the data:")
    print(data['data'][:5])  # Print the first 5 items from the response
else:
    print(f"API Request Failed. Status Code: {response.status_code}")
    print(response.text)



##Here we will be generating the coin_universe file that will contian all the coins and their data

import csv

# Save to CSV
with open("coin_universe.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "name", "symbol", "rank"])  # Header row
    for coin in data["data"]:
        writer.writerow([coin["id"], coin["name"], coin["symbol"], coin.get("rank", "N/A")])

print("Coin universe saved to 'coin_universe.csv'")


