from playwright.sync_api import sync_playwright
from loguru import logger
from typing import List, Dict
import time

def run_dynamic_scraper(base_url: str = "http://quotes.toscrape.com/js") -> List[Dict]:
    """
    Scrapes quotes from the JavaScript version of quotes.toscrape.com.
    Uses Playwright to render the page.
    """
    logger.info(f"Starting Dynamic Scraper (Playwright) on {base_url}...")
    data = []
    
    with sync_playwright() as p:
        # Launch browser (headless by default)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        current_page_num = 1
        while True:
            url = f"{base_url}/page/{current_page_num}/"
            logger.info(f"Navigating to {url}")
            page.goto(url)
            
            # Wait for quotes to load
            try:
                page.wait_for_selector(".quote", timeout=5000)
            except Exception:
                logger.info("No quotes found or timeout reached.")
                break
            
            quotes = page.query_selector_all(".quote")
            if not quotes:
                break
                
            for quote_card in quotes:
                text_el = quote_card.query_selector(".text")
                author_el = quote_card.query_selector(".author")
                tags_els = quote_card.query_selector_all(".tag")
                
                text = text_el.inner_text() if text_el else ""
                author = author_el.inner_text() if author_el else ""
                tags = [t.inner_text() for t in tags_els]
                
                data.append({
                    "type": "dynamic",
                    "text": text,
                    "author": author,
                    "tags": ", ".join(tags)
                })
            
            # Check for next button
            next_btn = page.query_selector(".pager .next > a")
            if not next_btn or current_page_num >= 3: # Limit for demo
                logger.info("Stopping dynamic scrape.")
                break
                
            current_page_num += 1
            
        browser.close()
        
    logger.success(f"Dynamic Scraper finished. Collected {len(data)} items.")
    return data
