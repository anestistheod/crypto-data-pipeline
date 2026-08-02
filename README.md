# 🚀 Automated Crypto Market Data Pipeline (ETL & Analytics)

An end-to-end Data Engineering pipeline built with Python, PostgreSQL, and Docker. This project extracts real-time cryptocurrency market data from a public REST API, transforms and cleanses the raw JSON payloads using Pandas, loads them into a normalized PostgreSQL schema, and performs time-series analytics using Advanced SQL Window Functions.

---

## 🏗️ Architecture & Data Flow

```text
[ Public REST API ] (CoinGecko API)
         │
         ▼
[ Extract Layer ] (Python `requests` + Error Handling)
         │
         ▼
[ Transform Layer ] (Pandas Data Cleansing & UTC Normalization)
         │
         ▼
[ Load Layer ] (SQLAlchemy Bulk Upsert)
         │
         ▼
[ Storage Layer ] (PostgreSQL running inside Docker Container)
         │
         ▼
[ Analytics Layer ] (Advanced SQL Window Functions - Moving Averages & LAG)
```

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.10+
* **Data Transformation:** Pandas
* **Database & Storage:** PostgreSQL 15, SQLAlchemy, `psycopg2`
* **Infrastructure & Containerization:** Docker, Docker Compose
* **Analytics:** Advanced SQL (Window Functions: `LAG`, `AVG() OVER()`, `PARTITION BY`)

---

## 📊 Database Schema

The PostgreSQL database follows a normalized **Dimension & Fact Table** architecture:

* **`assets` (Dimension Table):** Stores metadata about cryptocurrency assets (`asset_id`, `symbol`, `name`).
* **`market_data` (Fact Time-Series Table):** Stores price snapshots, 24-hour volume, and market cap timestamped in UTC. High-performance composite indexes are applied on `(asset_id, timestamp)`.

---

## 🚦 Getting Started

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
* Python 3.10+ installed

### 1. Clone the Repository

```bash
git clone https://github.com/anestistheod/crypto-data-pipeline.git
cd crypto-data-pipeline
```

### 2. Set Up Virtual Environment & Install Dependencies

```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Spin Up the Database Container

```bash
docker compose up -d
```

*This command automatically initializes the PostgreSQL database and executes `sql/init_schema.sql`.*

### 4. Run the Pipeline

```bash
python main.py
```

---

## 📈 Analytics & Sample SQL Output

The project includes pre-written analytical queries (`sql/analytics.sql`) leveraging SQL Window Functions to compute 3-period moving averages and interval price percentage changes:

```sql
SELECT
a.name AS asset_name,
m.timestamp,
m.price_usd,
LAG(m.price_usd, 1) OVER (PARTITION BY m.asset_id ORDER BY m.timestamp ASC) AS prev_price,
AVG(m.price_usd) OVER (PARTITION BY m.asset_id ORDER BY m.timestamp ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3_periods
FROM market_data m
JOIN assets a ON m.asset_id = a.asset_id;
```