-- Query 1: Υπολογισμός Κινούμενου Μέσου Όρου (Moving Average) & Ποσοστιαίας Μεταβολής (Price Change)
-- Χρήση Window Functions: LAG(), AVG() OVER()

SELECT 
    a.name AS asset_name,
    m.timestamp,
    m.price_usd,
    -- Προηγούμενη τιμή του ίδιου νομίσματος
    LAG(m.price_usd, 1) OVER (
        PARTITION BY m.asset_id 
        ORDER BY m.timestamp ASC
    ) AS previous_price,
    -- Ποσοστιαία μεταβολή από μέτρηση σε μέτρηση
    ROUND(
        ((m.price_usd - LAG(m.price_usd, 1) OVER (PARTITION BY m.asset_id ORDER BY m.timestamp ASC)) 
        / LAG(m.price_usd, 1) OVER (PARTITION BY m.asset_id ORDER BY m.timestamp ASC)) * 100, 
        4
    ) AS price_change_pct,
    -- Κινούμενος Μέσος Όρος των τελευταίων 3 μετρήσεων
    AVG(m.price_usd) OVER (
        PARTITION BY m.asset_id 
        ORDER BY m.timestamp ASC 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3_periods
FROM market_data m
JOIN assets a ON m.asset_id = a.asset_id
ORDER BY a.name, m.timestamp DESC;