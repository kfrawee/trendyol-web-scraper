import logging
import json
import os
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from constants import DEBUG, OUTPUTS_DIR, HEADLESS

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.name = "SCRAPER"


def dump_data(filename: str, data: str) -> None:
    if not os.path.exists(OUTPUTS_DIR):
        os.mkdir(OUTPUTS_DIR)
    if filename.endswith(".json"):
        with open(
            os.path.join(OUTPUTS_DIR, filename),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        with open(os.path.join(OUTPUTS_DIR, filename), "w", encoding="utf-8") as f:
            f.write(data)


def init_driver(headless: bool = HEADLESS) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    if headless:
        options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )

    return driver


def bypass_campaigns(driver: webdriver.Chrome) -> webdriver.Chrome:
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "campaign-button"))
        ).click()
    except Exception as e:
        # maybe there is no campaign \(-_-)/
        logger.warning(f"Failed to bypass campaigns. Error: {e}")
    return driver


def parse_value(value: str) -> float:
    return float(re.sub("[^0-9,.]", "", value).replace(",", "."))
