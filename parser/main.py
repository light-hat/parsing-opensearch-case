import logging
import os
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

driver = webdriver.Remote(command_executor=SELENIUM_REMOTE_URL, options=chrome_options)

try:
    driver.get("https://timeweb.cloud")

    # Ожидание загрузки контента
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    logging.info("Page loaded successfully")

    # Эмуляция человеческого поведения
    human_like_interaction(driver)

    # Получение информации о странице
    current_url = driver.current_url
    page_source = driver.page_source

    # Получение HTTP-статуса через JavaScript
    status_code = (
        driver.execute_script(
            "return window.performance.getEntries()[0].responseStatus || 200"
        )
        or 200
    )

    # Получение Content-Type
    content_type = driver.execute_script("return document.contentType || 'text/html'")

    # Извлечение первых 30 символов контента
    content_sample = page_source[:30].replace("\n", " ").replace("\r", " ")

    # Вывод результатов
    print(f"\n[+] Final URL: {current_url}")
    print(f"    Status: {status_code}")
    print(f"    Content-Type: {content_type}")
    print(f"    Content Sample: {content_sample}")

except Exception as e:
    logging.error(f"Error during crawling: {str(e)}")
    # Попытка сделать скриншот для отладки
    try:
        driver.save_screenshot("error_screenshot.png")
        logging.info("Saved screenshot to error_screenshot.png")
    except:
        logging.error("Failed to save screenshot")

finally:
    # Случайная задержка перед закрытием
    time.sleep(random.uniform(2.0, 5.0))
    driver.quit()
    logging.info("WebDriver closed")
