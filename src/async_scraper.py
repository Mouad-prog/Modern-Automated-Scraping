import asyncio
import httpx
from bs4 import BeautifulSoup
from loguru import logger
from typing import List, Dict

async def fetch_page(client, url):
    resp = await client.get(url)
    return resp.text

def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")
    books = soup.select("article.product_pod")
    data = []
    for book in books:
        title = book.select_one("h3 a")["title"]
        price = book.select_one(".price_color").get_text(strip=True)
        availability = book.select_one(".instock.availability").get_text(strip=True)
        data.append({
            "type": "async_books",
            "title": title,
            "price": price,
            "availability": availability
        })
    return data

async def run_async_scraper(base_url: str = "http://books.toscrape.com") -> List[Dict]:
    """
    Scrapes books from books.toscrape.com using async httpx.
    Fetches multiple pages concurrently.
    """
    logger.info(f"Starting Async Scraper on {base_url}...")
    
    # Generate URLs to scrape (e.g., first 5 pages)
    urls = [f"{base_url}/catalogue/page-{i}.html" for i in range(1, 6)]
    
    results = []
    
    async with httpx.AsyncClient() as client:
        tasks = [fetch_page(client, url) for url in urls]
        logger.info(f"Firing {len(tasks)} concurrent requests...")
        
        # Gather responses concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, response_text in enumerate(responses):
            if isinstance(response_text, Exception):
                logger.error(f"Error fetching page {i+1}: {response_text}")
                continue
            
            page_data = parse_books(response_text)
            results.extend(page_data)
            
    logger.success(f"Async Scraper finished. Collected {len(results)} books.")
    return results

if __name__ == "__main__":
    # Test run
    data = asyncio.run(run_async_scraper())
    print(data[:2])
