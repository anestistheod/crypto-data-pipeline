-- Create Assets table (Dimension Table)
CREATE TABLE IF NOT EXISTS assets (
    asset_id VARCHAR(50) PRIMARY KEY,       -- e.g. 'bitcoin', 'ethereum'
    symbol VARCHAR(10) NOT NULL,            -- e.g. 'btc', 'eth'
    name VARCHAR(100) NOT NULL,             -- e.g. 'Bitcoin', 'Ethereum'
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create Market Data table (Fact Table / Time-Series)
CREATE TABLE IF NOT EXISTS market_data (
    asset_id VARCHAR(50) REFERENCES assets(asset_id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL,
    price_usd NUMERIC(18, 8) NOT NULL,      -- Precision: 18 digits, 8 decimals (suitable for financial data)
    volume_24h NUMERIC(24, 2),
    market_cap NUMERIC(24, 2),
    PRIMARY KEY (asset_id, timestamp)       -- Composite primary key (Composite PK)
);

-- Create indexes for faster queries & analytics
CREATE INDEX IF NOT EXISTS idx_market_data_timestamp ON market_data(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_market_data_asset_time ON market_data(asset_id, timestamp DESC);