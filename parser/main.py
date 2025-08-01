import logging
import os
import random
import subprocess
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-webrtc")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://172.18.0.4:4444/wd/hub")
TEST_GET_URL = os.getenv("TEST_URL", "https://timeweb.cloud")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_selenium_get():

    driver = webdriver.Remote(
        command_executor=SELENIUM_REMOTE_URL, options=chrome_options
    )

    try:
        driver.get(TEST_GET_URL)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logging.info("Page loaded successfully")

        current_url = driver.current_url
        page_source = driver.page_source

        status_code = (
            driver.execute_script(
                "return window.performance.getEntries()[0].responseStatus || 200"
            )
            or 200
        )

        content_type = driver.execute_script(
            "return document.contentType || 'text/html'"
        )

        content_sample = page_source.replace("\n", " ").replace("\r", " ")

        print(f"\n[+] Final URL: {current_url}")
        print(f"    Status: {status_code}")
        print(f"    Content-Type: {content_type}")
        print(f"    Content Sample: {content_sample}")

    except Exception as e:
        logging.error(f"Error during crawling: {str(e)}")

        try:
            driver.save_screenshot("error_screenshot.png")
            logging.info("Saved screenshot to error_screenshot.png")
        except:
            logging.error("Failed to save screenshot")

    finally:
        time.sleep(random.uniform(2.0, 5.0))
        driver.quit()
        logging.info("WebDriver closed")


if __name__ == "__main__":
    test_selenium_get()
