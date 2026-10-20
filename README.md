# CodeAlpha Internship — Task 1: Web Scraping

## Project title
**E-Commerce-Style Book Data Scraper Using Python**

## Objective
This project demonstrates web scraping by collecting publicly available book information from **Books to Scrape**, a website created for scraping practice. The results are saved in a CSV file that can be opened in Excel or used for later data analysis.

## Data collected
- Book title
- Price
- Currency
- Availability
- Star-rating category
- Product page URL

## Tools
- Python
- Requests — sends HTTP requests to the website
- BeautifulSoup — parses HTML and extracts information
- CSV — stores the dataset in a spreadsheet-friendly format

## Project structure

```text
CodeAlpha_WebScraping/
├── scraper.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── .gitkeep
```

After running the scraper, `data/books_dataset.csv` will be created automatically.

## Setup in VS Code

1. Install Python 3.10 or newer.
2. Extract this ZIP file.
3. Open the extracted `CodeAlpha_WebScraping` folder in VS Code.
4. Open **Terminal → New Terminal**.
5. (Recommended) Create a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   If PowerShell blocks activation, you can skip activation and use `python -m pip` commands below.

6. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the project

Scrape all available practice pages:

```bash
python scraper.py
```

Scrape only the first 3 pages:

```bash
python scraper.py --max-pages 3
```

Choose a different output path:

```bash
python scraper.py --max-pages 2 --output data/sample_books.csv
```

## Expected output
The terminal displays progress and the number of books collected. The CSV file is saved at:

`data/books_dataset.csv`

Open that file with Microsoft Excel, LibreOffice Calc, or a text editor.

## How it works
1. Requests downloads a page from the practice website.
2. BeautifulSoup parses the HTML.
3. CSS selectors locate the book cards and their fields.
4. The script follows the site's **Next** link to scrape additional pages.
5. The collected records are written to a CSV file.

## Notes
- An internet connection is required when running the scraper.
- The included CSV is generated when you run the script; this ZIP does not contain fabricated scraping results.
- This is a practice project. For other websites, review their terms, robots.txt, access restrictions, and applicable laws before collecting data. Do not bypass logins, CAPTCHAs, or technical restrictions.
- If the site is temporarily unavailable, retry later.

## Internship submission checklist
- [ ] Run the script successfully.
- [ ] Confirm `data/books_dataset.csv` was created.
- [ ] Open the CSV and inspect the rows.
- [ ] Add screenshots of the terminal and CSV output to your project documentation if required.
- [ ] Upload the project to a GitHub repository named `CodeAlpha_WebScraping` (or the exact name specified by your coordinator).
- [ ] Submit the repository link using the official internship submission form.

## Learning outcomes
This project practices HTTP requests, HTML parsing, CSS selectors, pagination, error handling, CSV creation, and basic data collection.
