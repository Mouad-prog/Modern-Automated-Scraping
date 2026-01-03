# Modern Automated Scraping Project

This project demonstrates a robust, multi-strategy approach to web scraping using Python. It implements three different scraping methodologies to handle various real-world scenarios, from simple static pages to complex JavaScript-rendered applications.

## 🚀 Features

The project consists of three independent modules orchestrator by a central script:

1.  **Static Scraper** (`src/static_scraper.py`)
    *   **Technology**: `httpx`, `BeautifulSoup`
    *   **Use Case**: Fast, lightweight scraping for standard server-side rendered websites.
    *   **Target**: [quotes.toscrape.com](http://quotes.toscrape.com)

2.  **Dynamic Scraper** (`src/dynamic_scraper.py`)
    *   **Technology**: `Playwright` (Headless Browser)
    *   **Use Case**: Handling modern single-page applications (SPAs) or sites that rely on JavaScript to render content.
    *   **Target**: [quotes.toscrape.com/js](http://quotes.toscrape.com/js)

3.  **Async/High-Performance Scraper** (`src/async_scraper.py`)
    *   **Technology**: `httpx` (Async), `asyncio`
    *   **Use Case**: High-concurrency scraping to fetch large amounts of data quickly by making parallel requests.
    *   **Target**: [books.toscrape.com](http://books.toscrape.com)

## 🛠️ Installation

1.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Install Browser Binaries** (for Playwright):
    ```bash
    playwright install
    ```

## ▶️ Usage

Run the main orchestration script to access the interactive menu:

```bash
python main.py
```

You will be presented with the following options:
1.  **Static Scraper**: Scrape quotes normally.
2.  **Dynamic Scraper**: Scrape quotes using a headless browser.
3.  **Async Scraper**: concurrently scrape book data.
4.  **Run All**: Execute all scrapers in sequence.

## 📂 Output

All scraped data is automatically saved to the `data/` directory in two formats:
*   **CSV** (`_dataset.csv`)
*   **JSON** (`_dataset.json`)

## 📁 Project Structure

```
project/
├── data/               # Output datasets
├── logs/               # Execution logs
├── src/
│   ├── static_scraper.py
│   ├── dynamic_scraper.py
│   └── async_scraper.py
├── main.py             # Entry point
└── requirements.txt    # Project dependencies
```
