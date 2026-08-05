import requests
import logging
from typing import List, Dict, Any

# Logging setup for monitoring the flow
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Public CoinGecko API endpoint
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_crypto_data(crypto_ids: List[str], vs_currency: str = "usd") -> List[Dict[str, Any]]:
    """
    Fetches market data for a list of cryptocurrencies from the CoinGecko API.

    :param crypto_ids: List of IDs (e.g., ['bitcoin', 'ethereum', 'solana'])
    :param vs_currency: Comparison currency (default: 'usd')
    :return: List of dictionaries containing the raw JSON data
    """
    params = {
        "vs_currency": vs_currency,
        "ids": ",".join(crypto_ids),
        "order": "market_cap_desc",
        "per_page": len(crypto_ids),
        "page": 1,
        "sparkline": False
    }

    try:
        logging.info(f"Fetching data from API for: {crypto_ids}...")
        response = requests.get(COINGECKO_URL, params=params, timeout=10)

        # Check if the call was successful (HTTP status code 200)
        response.raise_for_status()

        data = response.json()
        logging.info(f"Successful retrieval of {len(data)} records from the API.")
        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"Error when calling the API: {e}")
        return []


# Quick Test: Run this file standalone for verification
if __name__ == "__main__":
    target_coins = ["bitcoin", "ethereum", "cardano", "solana"]
    raw_data = fetch_crypto_data(target_coins)

    if raw_data:
        print("\n--- Example First Record ---")
        print(f"ID: {raw_data[0]['id']}")
        print(f"Symbol: {raw_data[0]['symbol']}")
        print(f"Price USD: ${raw_data[0]['current_price']}")
        print(f"Market Cap: ${raw_data[0]['market_cap']}")
