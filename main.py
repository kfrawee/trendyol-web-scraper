from utils import *

from constants import BASE_URL, PRODUCT_URL
from datetime import datetime
import time
from urllib.parse import urljoin


def main():
    start = time.time()
    data = {}

    driver = init_driver()
    driver.get(PRODUCT_URL)
    bypass_campaigns(driver)

    current_html = driver.page_source
    main_soup = BeautifulSoup(current_html, "html.parser")

    product_title = main_soup.find("h1", {"class": "pr-new-br"}).span.text
    data.update(product_title=product_title)

    product_categories = main_soup.find_all("a", {"class": "slc-img"})

    categories_temp_dict = {}
    for category in product_categories:
        categories_temp_dict[category["title"]] = urljoin(BASE_URL, category["href"])


    data.update(product_categories=list(categories_temp_dict.keys()))
    categories_data = {}

    # selected category at 0 index
    for k, v in categories_temp_dict.items():
        selected_category_name, selected_category_url = k, v
        break

    category_price_soap = main_soup.find("div", {"class": "product-price-container"})
    category_price_info = category_price_soap.find(
        "div", {"class": "featured-price-info"}
    ).text
    category_price_value = category_price_soap.find(
        "div", {"class": "featured-prices"}
    ).text
    category_selected_size = main_soup.find(
        "span", {"class": "size-variant-attr-value"}
    ).text
    available_sizes_soup = main_soup.find_all("div", {"class": "sp-itm"})
    available_sizes = [size_soap.text for size_soap in available_sizes_soup]

    other_sizes_data = []
    for size_soap in available_sizes_soup:
        if size_soap.text == category_selected_size:
            continue

        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//div[text()="{size_soap.text}"]')
                )
            )

            element.click()

            current_html = driver.page_source
            soup = BeautifulSoup(current_html, "html.parser")
            category_price_value = soup.find("div", {"class": "featured-prices"}).text

            other_sizes_data.append(
                {
                    "size_name": size_soap.text,
                    "size_price_info": category_price_info,
                    "size_price_value": parse_value(category_price_value),
                    "size_url": driver.current_url,
                }
            )
        except Exception as e:
            logger.warning(f"Failed to click on size: {e}")

    selected_category = {
        "category_name": selected_category_name,
        "category_url": selected_category_url,
        "category_price_info": category_price_info,
        "category_price_value": parse_value(category_price_value),
        "selected_size": category_selected_size,
        "available_sizes": available_sizes,
        "other_sizes_date": other_sizes_data,
    }
    categories_data.update(selected_category=selected_category)

    # other categories
    driver.quit()

    other_categories = []
    for category_name, category_url in categories_temp_dict.items():
        if category_name == selected_category_name:
            continue
        driver = init_driver()
        driver.get(category_url)
        bypass_campaigns(driver)
        

        current_html = driver.page_source
        main_soup = BeautifulSoup(current_html, "html.parser")

        category_price_soap = main_soup.find(
            "div", {"class": "product-price-container"}
        )
        category_price_value = category_price_soap.text

        category_selected_size = main_soup.find(
            "span", {"class": "size-variant-attr-value"}
        ).text
        available_sizes_soup = main_soup.find_all("div", {"class": "sp-itm"})
        available_sizes = [size_soap.text for size_soap in available_sizes_soup]

        other_sizes_data = []
        for size_soap in available_sizes_soup:
            if size_soap.text == category_selected_size:
                continue

            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f'//div[text()="{size_soap.text}"]')
                    )
                )

                element.click()

                current_html = driver.page_source
                soup = BeautifulSoup(current_html, "html.parser")
                price_soap = soup.find("div", {"class": "product-price-container"})
                category_price_value = price_soap.text
                other_sizes_data.append(
                    {
                        "size_name": size_soap.text,
                        "size_price_info": category_price_info,
                        "size_price_value": parse_value(category_price_value),
                        "size_url": driver.current_url,
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to click on size: {e}")

        other_categories.append(
            {
                "category_name": category_name,
                "category_url": category_url,
                "category_price_value": parse_value(category_price_value),
                "selected_size": category_selected_size,
                "available_sizes": available_sizes,
                "other_sizes_date": other_sizes_data,
            }
        )
        driver.quit()
    categories_data.update(other_categories=other_categories)

    data.update(categories_data=categories_data)
    data.update(timestamp=str(datetime.now()))

    dump_data("data.json", data)

    driver.quit()

    end = time.time()
    logger.info(f"Completed in {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
