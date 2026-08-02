-- Δημιουργία πίνακα Assets (Dimension Table)
CREATE TABLE IF NOT EXISTS assets (
    asset_id VARCHAR(50) PRIMARY KEY,       -- π.χ. 'bitcoin', 'ethereum'
    symbol VARCHAR(10) NOT NULL,            -- π.χ. 'btc', 'eth'
    name VARCHAR(100) NOT NULL,             -- π.χ. 'Bitcoin', 'Ethereum'
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Δημιουργία πίνακα Market Data (Fact Table / Time-Series)
CREATE TABLE IF NOT EXISTS market_data (
    asset_id VARCHAR(50) REFERENCES assets(asset_id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL,
    price_usd NUMERIC(18, 8) NOT NULL,      -- Ακρίβεια 18 ψηφίων, 8 δεκαδικά (κατάλληλο για οικονομικά δεδομένα)
    volume_24h NUMERIC(24, 2),
    market_cap NUMERIC(24, 2),
    PRIMARY KEY (asset_id, timestamp)       -- Σύνθετο πρωτεύον κλειδί (Composite PK)
);

-- Δημιουργία Indexes για ταχύτητα στα Queries & Analytics
CREATE INDEX IF NOT EXISTS idx_market_data_timestamp ON market_data(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_market_data_asset_time ON market_data(asset_id, timestamp DESC);