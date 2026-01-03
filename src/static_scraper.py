import httpx
from bs4 import BeautifulSoup
from loguru import logger
import pandas as pd
from typing import List, Dict

def run_static_scraper(base_url: str = "http://quotes.toscrape.com") -> List[Dict]:
    """
    Scrapes quotes from the static version of quotes.toscrape.com.
    Uses httpx for requests and BeautifulSoup for parsing.
    """
    logger.info(f"Starting Static Scraper on {base_url}...")
    
    data = []
    page = 1
    
    with httpx.Client() as client:
        while True:
            url = f"{base_url}/page/{page}/"
            logger.info(f"Fetching {url}")
            
            try:
                response = client.get(url)
                response.raise_for_status()
            except httpx.HTTPError as e:
                logger.error(f"HTTP error occurred: {e}")
                break
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            quotes = soup.select(".quote")
            if not quotes:
                logger.info("No more quotes found. Stopping.")
                break
                
            for quote_card in quotes:
                text = quote_card.select_one(".text").get_text(strip=True)
                author = quote_card.select_one(".author").get_text(strip=True)
                tags = [tag.get_text(strip=True) for tag in quote_card.select(".tags .tag")]
                
                data.append({
                    "type": "static",
                    "text": text,
                    "author": author,
                    "tags": ", ".join(tags)
                })
            
            # Limit pages for demo purposes
            if page >= 3: 
                logger.info("Reached page limit for demo.")
                break
                
            page += 1
            
    logger.success(f"Static Scraper finished. Collected {len(data)} items.")
    return data
