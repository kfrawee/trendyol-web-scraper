import os
from urllib.parse import urljoin

DEBUG = False
HEADLESS = False
OUTPUTS_DIR = os.path.join(os.getcwd(), "outputs")

BASE_URL = "https://www.trendyol.com/formeya/"
PRODUCT_URL = urljoin(
    BASE_URL,
    "mikro-fitted-full-kenar-su-sivi-gecirmez-yatak-koruyucu-alez-carsaf-tek-cift-battal-10-farkli-ebat-p-43257286",
)
