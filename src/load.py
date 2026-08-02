import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Στοιχεία σύνδεσης στη βάση (ίδια με αυτά στο docker-compose.yml)
DB_USER = os.getenv("DB_USER", "data_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "my_secure_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "crypto_analytics")

# Δημιουργία SQLAlchemy Database Engine
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_db_engine() -> Engine:
    """Δημιουργεί και επιστρέφει το SQLAlchemy Engine."""
    return create_engine(DATABASE_URL)


def load_assets(engine: Engine, assets_df: pd.DataFrame) -> None:
    """
    Εισάγει τα assets στη βάση. 
    Χρησιμοποιεί ON CONFLICT DO NOTHING για να αποφύγει σφάλματα αν το asset υπάρχει ήδη.
    """
    if assets_df.empty:
        return

    query = text("""
        INSERT INTO assets (asset_id, symbol, name)
        VALUES (:asset_id, :symbol, :name)
        ON CONFLICT (asset_id) DO NOTHING;
    """)

    records = assets_df.to_dict(orient="records")

    with engine.begin() as connection:
        connection.execute(query, records)

    logging.info(
        f"Επιτυχής φόρτωση/ενημέρωση {len(records)} εγγραφών στον πίνακα 'assets'.")


def load_market_data(engine: Engine, market_data_df: pd.DataFrame) -> None:
    """
    Αποθηκεύει τις μετρήσεις τιμών στον πίνακα market_data.
    """
    if market_data_df.empty:
        return

    # Χρήση της to_sql του Pandas για μαζική εγγραφή (Bulk Insert)
    market_data_df.to_sql(
        name="market_data",
        con=engine,
        if_exists="append",  # Προσθήκη νέων εγγραφών χωρίς διαγραφή του πίνακα
        index=False,
        method="multi"
    )
    logging.info(
        f"Επιτυχής εγγραφή {len(market_data_df)} νέων μετρήσεων στον πίνακα 'market_data'.")


# Quick Test: Αυτόνομη εκτέλεση του load μαζί με extract & transform
if __name__ == "__main__":
    from extract import fetch_crypto_data
    from transform import transform_crypto_data

    logging.info("--- Εκκίνηση Δοκιμαστικής Ροής Load ---")

    # 1. Extract
    target_coins = ["bitcoin", "ethereum", "solana", "cardano"]
    raw = fetch_crypto_data(target_coins)

    # 2. Transform
    assets_df, market_df = transform_crypto_data(raw)

    # 3. Load στη PostgreSQL
    db_engine = get_db_engine()
    load_assets(db_engine, assets_df)
    load_market_data(db_engine, market_df)

    logging.info("--- Η διαδικασία Load ολοκληρώθηκε επιτυχώς! ---")
