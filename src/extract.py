import requests
import logging
from typing import List, Dict, Any

# Ρύθμιση logging για παρακολούθηση της ροής
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Δημόσιο API endpoint της CoinGecko
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_crypto_data(crypto_ids: List[str], vs_currency: str = "usd") -> List[Dict[str, Any]]:
    """
    Τραβάει δεδομένα αγοράς για μια λίστα από κρυπτονομίσματα από το CoinGecko API.

    :param crypto_ids: Λίστα με τα IDs (π.χ. ['bitcoin', 'ethereum', 'solana'])
    :param vs_currency: Νόμισμα σύγκρισης (default: 'usd')
    :return: Λίστα από λεξικά (dictionaries) με τα raw JSON δεδομένα
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
        logging.info(f"Τράβηγμα δεδομένων από το API για: {crypto_ids}...")
        response = requests.get(COINGECKO_URL, params=params, timeout=10)

        # Έλεγχος αν η κλήση ήταν επιτυχής (HTTP status code 200)
        response.raise_for_status()

        data = response.json()
        logging.info(f"Επιτυχής λήψη {len(data)} εγγραφών από το API.")
        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"Σφάλμα κατά την κλήση στο API: {e}")
        return []


# Quick Test: Εκτέλεση του αρχείου αυτόνομα για επιβεβαίωση
if __name__ == "__main__":
    target_coins = ["bitcoin", "ethereum", "cardano", "solana"]
    raw_data = fetch_crypto_data(target_coins)

    if raw_data:
        print("\n--- Παράδειγμα Πρώτης Εγγραφής ---")
        print(f"ID: {raw_data[0]['id']}")
        print(f"Symbol: {raw_data[0]['symbol']}")
        print(f"Price USD: ${raw_data[0]['current_price']}")
        print(f"Market Cap: ${raw_data[0]['market_cap']}")
