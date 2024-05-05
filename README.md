# Basic Selenium web scraper:
> Simple web scraper using selenium, because the website it using JS to fetch the data.

## How to run:
- Clone the repository

    `git clone https://github.com/kfrawee/trendyol-web-scraper.git && cd trendyol-web-scraper`

- Create virtual environment:

    `python -m venv .venv && source .venv/bin/activate`

- Install dependencies:

    `pip install -r requirements.txt`

- Run the scrip:

    `python main.py`

- Final data should be found under: `/outputs/data.json`

## 
In `constants.py` You might want to change:
- `DEBUG = False` to disable console debug logs statements.
- `HEADLESS = False` to run selenium in headless mode (without GUI).

