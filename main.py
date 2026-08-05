import logging
from src.extract import fetch_crypto_data
from src.transform import transform_crypto_data
from src.load import get_db_engine, load_assets, load_market_data

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)


def run_pipeline():
    logging.info("==========================================")
    logging.info("  Starting Crypto Data Pipeline (ETL)     ")
    logging.info("==========================================")

    # Target coins to monitor
    target_coins = ["bitcoin", "ethereum", "solana", "cardano", "ripple"]

    try:
        # Step 1: Extract
        logging.info("Step 1/3: Extracting data from API...")
        raw_data = fetch_crypto_data(target_coins)
        if not raw_data:
            logging.error("Pipeline stopped: No data fetched from API.")
            return

        # Step 2: Transform
        logging.info("Step 2/3: Transforming data with Pandas...")
        assets_df, market_df = transform_crypto_data(raw_data)

        # Step 3: Load
        logging.info("Step 3/3: Loading data into PostgreSQL...")
        db_engine = get_db_engine()
        load_assets(db_engine, assets_df)
        load_market_data(db_engine, market_df)

        logging.info("==========================================")
        logging.info("  ETL Pipeline Completed Successfully!    ")
        logging.info("==========================================")

    except Exception as e:
        logging.critical(
            f"Pipeline failed with unhandled exception: {e}", exc_info=True)


if __name__ == "__main__":
    run_pipeline()
