-- Query 1: Calculate Moving Average (MA) & Price Change
-- Using window functions: LAG(), AVG() OVER()

SELECT 
    a.name AS asset_name,
    m.timestamp,
    m.price_usd,
    -- Previous price for the same asset
    LAG(m.price_usd, 1) OVER (
        PARTITION BY m.asset_id 
        ORDER BY m.timestamp ASC
    ) AS previous_price,
    -- Percentage change between consecutive measurements
    ROUND(
        ((m.price_usd - LAG(m.price_usd, 1) OVER (PARTITION BY m.asset_id ORDER BY m.timestamp ASC)) 
        / LAG(m.price_usd, 1) OVER (PARTITION BY m.asset_id ORDER BY m.timestamp ASC)) * 100, 
        4
    ) AS price_change_pct,
    -- Moving average of the last 3 measurements
    AVG(m.price_usd) OVER (
        PARTITION BY m.asset_id 
        ORDER BY m.timestamp ASC 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3_periods
FROM market_data m
JOIN assets a ON m.asset_id = a.asset_id
ORDER BY a.name, m.timestamp DESC;