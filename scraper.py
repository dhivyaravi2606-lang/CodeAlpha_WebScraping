"""
CodeAlpha Internship - Task 1: Web Scraping
Project: Books to Scrape Product Data Collector

Collects book title, price, availability, rating, and product URL from the
public practice website https://books.toscrape.com/ and saves the results
to data/books_dataset.csv.

Usage:
    python scraper.py
    python scraper.py --pages 3
    python scraper.py --max-pages 5 --output data/my_books.csv
"""

import argparse
import csv
import logging
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = PROJECT_DIR / "data" / "books_dataset.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}
FIELDS = [
    "book_title",
    "price",
    "currency",
    "availability",
    "rating",
    "product_url",
]


def get_soup(session: requests.Session, url: str) -> BeautifulSoup:
    """Fetch a page and return parsed HTML; raises a clear error on failure."""
    response = session.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_book(card, page_url: str) -> dict:
    """Extract fields from one book card."""
    title_link = card.select_one("h3 a")
    price_element = card.select_one(".price_color")
    availability_element = card.select_one(".availability")
    rating_element = card.select_one("p.star-rating")

    title = title_link.get("title", "").strip() if title_link else ""
    product_url = urljoin(page_url, title_link.get("href", "")) if title_link else ""
    raw_price = price_element.get_text(" ", strip=True) if price_element else ""
    # Keep the numeric price as a text field and identify its currency separately.
    cleaned_price = re.sub(r"[^\d.]", "", raw_price)
    currency = "GBP" if "£" in raw_price else ""

    availability = (
        " ".join(availability_element.get_text(" ", strip=True).split())
        if availability_element
        else "Unknown"
    )

    rating_classes = rating_element.get("class", []) if rating_element else []
    rating = next(
        (item for item in rating_classes if item in {"One", "Two", "Three", "Four", "Five"}),
        "Unknown",
    )

    return {
        "book_title": title,
        "price": cleaned_price,
        "currency": currency,
        "availability": availability,
        "rating": rating,
        "product_url": product_url,
    }


def scrape_books(max_pages: int = 0, delay: float = 0.5) -> list[dict]:
    """
    Scrape book cards across pages.
    max_pages=0 means continue until the website has no next page.
    A small delay is used between requests.
    """
    records = []
    current_url = BASE_URL
    pages_scraped = 0

    with requests.Session() as session:
        while current_url:
            if max_pages and pages_scraped >= max_pages:
                break

            logger.info("Scraping page %s: %s", pages_scraped + 1, current_url)
            soup = get_soup(session, current_url)
            cards = soup.select("article.product_pod")

            if not cards:
                logger.warning("No book cards found on this page.")
                break

            for card in cards:
                records.append(parse_book(card, current_url))

            pages_scraped += 1
            next_link = soup.select_one("li.next a")
            current_url = urljoin(current_url, next_link["href"]) if next_link else ""

            if current_url and (not max_pages or pages_scraped < max_pages):
                time.sleep(max(0.0, delay))

    return records


def save_csv(records: list[dict], output_path: Path) -> None:
    """Write scraped records to a UTF-8 CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect book information from Books to Scrape."
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Maximum pages to scrape. Use 0 to scrape all available pages (default).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay in seconds between page requests (default: 0.5).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="CSV output path (default: data/books_dataset.csv).",
    )
    args = parser.parse_args()

    if args.max_pages < 0:
        parser.error("--max-pages must be 0 or a positive integer.")
    if args.delay < 0:
        parser.error("--delay cannot be negative.")

    try:
        records = scrape_books(max_pages=args.max_pages, delay=args.delay)
        if not records:
            logger.error("No records collected. Check your internet connection or website access.")
            raise SystemExit(1)

        save_csv(records, args.output)
        logger.info("Completed successfully.")
        logger.info("Pages/records collected: %s books", len(records))
        logger.info("CSV saved to: %s", args.output.resolve())
        logger.info("First book: %s", records[0]["book_title"])
    except requests.RequestException as exc:
        logger.error("Could not access the practice website: %s", exc)
        logger.error("Check your internet connection and try again.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
