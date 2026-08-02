import pandas as pd
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def transform_crypto_data(raw_data: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Μετασχηματίζει τα raw JSON δεδομένα του API σε δύο καθαρά Pandas DataFrames
    που αντιστοιχούν στους πίνακες 'assets' και 'market_data' της βάσης.

    :param raw_data: Λίστα από dictionaries από το API
    :return: Τριάδα (assets_df, market_data_df)
    """
    if not raw_data:
        logging.warning("Δεν βρέθηκαν δεδομένα για μετασχηματισμό.")
        return pd.DataFrame(), pd.DataFrame()

    # Μετατροπή της λίστας JSON σε αρχικό Pandas DataFrame
    df = pd.DataFrame(raw_data)

    # 1. Transform για τον πίνακα ASSETS (Dimension Table)
    assets_df = df[['id', 'symbol', 'name']].copy()
    assets_df.rename(columns={'id': 'asset_id'}, inplace=True)
    assets_df['symbol'] = assets_df['symbol'].str.lower()

    # Αφαίρεση διπλότυπων αν υπάρχουν
    assets_df.drop_duplicates(subset=['asset_id'], inplace=True)

    # 2. Transform για τον πίνακα MARKET_DATA (Fact Table)
    market_data_df = df[['id', 'current_price',
                         'total_volume', 'market_cap']].copy()
    market_data_df.rename(columns={
        'id': 'asset_id',
        'current_price': 'price_usd',
        'total_volume': 'volume_24h'
    }, inplace=True)

    # Προσθήκη UTC Timestamp για την τρέχουσα στιγμή της μέτρησης
    current_utc_timestamp = datetime.now(timezone.utc)
    market_data_df['timestamp'] = current_utc_timestamp

    # Αναδιάταξη στηλών για να ταιριάζουν ακριβώς με το SQL Schema
    market_data_df = market_data_df[[
        'asset_id', 'timestamp', 'price_usd', 'volume_24h', 'market_cap']]

    # Διασφάλιση σωστών data types (Numeric Conversions)
    market_data_df['price_usd'] = pd.to_numeric(
        market_data_df['price_usd'], errors='coerce')
    market_data_df['volume_24h'] = pd.to_numeric(
        market_data_df['volume_24h'], errors='coerce')
    market_data_df['market_cap'] = pd.to_numeric(
        market_data_df['market_cap'], errors='coerce')

    logging.info(
        f"Επιτυχής μετασχηματισμός: {len(assets_df)} assets & {len(market_data_df)} market records.")

    return assets_df, market_data_df


# Quick Test: Αυτόνομη εκτέλεση του transform μαζί με το extract
if __name__ == "__main__":
    from extract import fetch_crypto_data

    target_coins = ["bitcoin", "ethereum", "solana"]
    raw = fetch_crypto_data(target_coins)

    assets_df, market_df = transform_crypto_data(raw)

    print("\n--- Assets DataFrame ---")
    print(assets_df)

    print("\n--- Market Data DataFrame ---")
    print(market_df.to_string())
