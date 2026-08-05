import pandas as pd
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def transform_crypto_data(raw_data: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Transforms raw JSON API data into two clean Pandas DataFrames
    corresponding to the 'assets' and 'market_data' tables.

    :param raw_data: List of dictionaries from the API
    :return: Tuple (assets_df, market_data_df)
    """
    if not raw_data:
        logging.warning("No data found for transformation.")
        return pd.DataFrame(), pd.DataFrame()

    # Convert the JSON list into an initial Pandas DataFrame
    df = pd.DataFrame(raw_data)

    # 1. Transform for the ASSETS table (Dimension Table)
    assets_df = df[['id', 'symbol', 'name']].copy()
    assets_df.rename(columns={'id': 'asset_id'}, inplace=True)
    assets_df['symbol'] = assets_df['symbol'].str.lower()

    # Remove duplicates if present
    assets_df.drop_duplicates(subset=['asset_id'], inplace=True)

    # 2. Transform for the MARKET_DATA table (Fact Table)
    market_data_df = df[['id', 'current_price',
                         'total_volume', 'market_cap']].copy()
    market_data_df.rename(columns={
        'id': 'asset_id',
        'current_price': 'price_usd',
        'total_volume': 'volume_24h'
    }, inplace=True)

    # Add UTC timestamp for the measurement time
    current_utc_timestamp = datetime.now(timezone.utc)
    market_data_df['timestamp'] = current_utc_timestamp

    # Reorder columns to exactly match the SQL schema
    market_data_df = market_data_df[[
        'asset_id', 'timestamp', 'price_usd', 'volume_24h', 'market_cap']]

    # Ensure correct data types (numeric conversions)
    market_data_df['price_usd'] = pd.to_numeric(
        market_data_df['price_usd'], errors='coerce')
    market_data_df['volume_24h'] = pd.to_numeric(
        market_data_df['volume_24h'], errors='coerce')
    market_data_df['market_cap'] = pd.to_numeric(
        market_data_df['market_cap'], errors='coerce')

    logging.info(
        f"Successful transform: {len(assets_df)} assets & {len(market_data_df)} market records.")

    return assets_df, market_data_df


# Quick Test: Standalone execution of transform with extract
if __name__ == "__main__":
    from extract import fetch_crypto_data

    target_coins = ["bitcoin", "ethereum", "solana"]
    raw = fetch_crypto_data(target_coins)

    assets_df, market_df = transform_crypto_data(raw)

    print("\n--- Assets DataFrame ---")
    print(assets_df)

    print("\n--- Market Data DataFrame ---")
    print(market_df.to_string())
