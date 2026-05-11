
# Amazon Product Scraper

A Scrapy-based web scraper that fetches Amazon product data (prices, discounts, coupons, availability) using ASINs stored in MongoDB, and updates the database with the scraped results.

---

## Project Structure

```
amazon-scraper/
├── whiskyscraper/
│   ├── spiders/
│   │   ├── __init__.py
│   │   ├── amazonSpider.py       # Spider for active products
│   │   └── amazonSpider2.py      # Spider for null/inactive products
│   ├── __init__.py
│   ├── items.py                  # Scrapy item definitions
│   ├── middlewares.py            # Proxy + User-Agent middleware
│   ├── pipelines.py              # CSV output pipelines
│   ├── settings.py               # Scrapy settings
│   └── database.py               # MongoDB read/write helpers
├── scripts/
│   └── download_products.sh      # SCP script to download CSV files
├── .env                          # Environment variables (never commit)
├── .env.example                  # Template for environment variables
├── .gitignore                    # Files excluded from git
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## Features

- Scrapes Amazon product pages using rotating proxies and user agents
- Extracts: title, price, deal discount, original price, coupon (% or $), subscription savings, final price, product image
- Handles unavailable products and moves them to a `null_products` MongoDB collection
- Retries up to 30 times per product if the page doesn't load correctly
- Outputs data to CSV files via Scrapy pipelines
- Updates MongoDB with scraped results after each product

---

## MongoDB Collections

| Collection        | Description                                      |
|-------------------|--------------------------------------------------|
| `products`        | Main product list with `scrape_status: 0` to scrape |
| `variant_products`| Product variants with pricing info              |
| `null_products`   | Products that are unavailable or not found      |

Each document requires at minimum:
- `ASIN` — Amazon Standard Identification Number
- `scrape_status` — `0` = pending, `1` = scraped

---

## Spiders

### `amazon` (`amazonSpider.py`)
Scrapes active products from the `products` collection. Extracts full deal info including coupons, subscription discounts, and images.

```bash
scrapy crawl amazon
```

### `amazon_non` (`amazonSpider2.py`)
Re-scrapes products from the `null_products` collection to check if they've become available again.

```bash
scrapy crawl amazon_non
```

---

## Output CSV Files

| File                | Description                            |
|---------------------|----------------------------------------|
| `product.csv`       | Full product deal data                 |
| `product_update.csv`| Update data for null products          |
| `coupon.csv`        | Coupon-specific data                   |
| `availability.csv`  | Products marked as currently unavailable |
| `amazon.csv`        | Raw Scrapy feed output                 |

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/amazon-scraper.git
cd amazon-scraper
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials (see `.env.example` for required keys).

### 5. Run a spider

```bash
scrapy crawl amazon
```

---

## Environment Variables

All secrets are stored in `.env` (never committed to git). See `.env.example` for the full list.

| Variable           | Description                              |
|--------------------|------------------------------------------|
| `MONGO_URI`        | MongoDB connection string                |
| `PROXY_USER`       | Proxy username                           |
| `PROXY_PASSWORD`   | Proxy password                           |
| `PROXY_ENDPOINT`   | Proxy host/endpoint                      |
| `PROXY_PORT`       | Proxy port                               |

---

## Notes

- Proxy rotation is handled by `MyProxyMiddleware` in `middlewares.py`
- User agents are rotated using the `latest-user-agents` package
- `ROBOTSTXT_OBEY` is set to `False` — ensure you comply with Amazon's Terms of Service
- Do **not** commit `.env`, `*.csv`, or any file containing credentials

---

