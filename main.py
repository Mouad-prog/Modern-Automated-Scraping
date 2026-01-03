import sys
import asyncio
import pandas as pd
from loguru import logger
import os

# Import scrapers
from src.static_scraper import run_static_scraper
from src.dynamic_scraper import run_dynamic_scraper
from src.async_scraper import run_async_scraper

DATA_DIR = "data"

def save_data(data, filename_prefix):
    if not data:
        logger.warning("No data to save.")
        return

    df = pd.DataFrame(data)
    
    # Ensure data dir exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    csv_path = os.path.join(DATA_DIR, f"{filename_prefix}_dataset.csv")
    json_path = os.path.join(DATA_DIR, f"{filename_prefix}_dataset.json")
    
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", lines=True)
    
    logger.info(f"Data saved to {csv_path} and {json_path}")

def main():
    logger.add("logs/scraper.log", rotation="1 MB")
    
    print("--- Modern Automated Scraping Project ---")
    print("1. Run Static Scraper (Quotes)")
    print("2. Run Dynamic Scraper (Quotes JS)")
    print("3. Run Async Scraper (Books)")
    print("4. Run All")
    print("0. Exit")
    
    choice = input("Select an option: ")
    
    if choice == "1":
        data = run_static_scraper()
        save_data(data, "static_quotes")
        
    elif choice == "2":
        data = run_dynamic_scraper()
        save_data(data, "dynamic_quotes")
        
    elif choice == "3":
        data = asyncio.run(run_async_scraper())
        save_data(data, "async_books")
        
    elif choice == "4":
        logger.info("Running ALL scrapers...")
        
        d1 = run_static_scraper()
        save_data(d1, "static_quotes")
        
        d2 = run_dynamic_scraper()
        save_data(d2, "dynamic_quotes")
        
        d3 = asyncio.run(run_async_scraper())
        save_data(d3, "async_books")
        
    elif choice == "0":
        sys.exit(0)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
