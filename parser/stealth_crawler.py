import logging
import os
import random
import sys
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_random_user_agent():
    return UserAgent().random


def configure_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--remote-debugging-address=0.0.0.0")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    return chrome_options


def human_like_interaction(driver):
    """Эмулирует человеческое поведение"""
    # Случайная прокрутка
    for _ in range(random.randint(1, 3)):
        scroll_distance = random.randint(200, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(0.5, 1.5))

    # Случайные движения мышью
    action = webdriver.ActionChains(driver)
    for _ in range(random.randint(2, 5)):
        action.move_by_offset(
            random.randint(-50, 50), random.randint(-50, 50)
        ).perform()
        time.sleep(random.uniform(0.2, 0.7))

    # Паузы между действиями
    time.sleep(random.uniform(1.0, 3.0))


def crawl_with_selenium(start_url):
    options = configure_chrome_options()

    try:
        # Используем системный ChromeDriver
        service = Service(executable_path="/usr/local/bin/chromedriver")

        driver = webdriver.Chrome(service=service, options=options)

        # Настройка параметров браузера
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        logging.info(f"Navigating to {start_url}")
        try:
            driver.get(start_url)

            # Ожидание загрузки контента
            WebDriverWait(driver, 20).until(
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
            content_type = driver.execute_script(
                "return document.contentType || 'text/html'"
            )

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

    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stealth_crawler.py <start_url>")
        sys.exit(1)

    start_url = sys.argv[1]
    crawl_with_selenium(start_url)
