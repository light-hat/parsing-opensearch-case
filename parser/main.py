import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-webrtc")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")

SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://172.18.0.4:4444/wd/hub")

driver = webdriver.Remote(
    command_executor=SELENIUM_REMOTE_URL,
    options=chrome_options
)

driver.get("https://www.timeweb.cloud")

time.sleep(9999)

driver.quit()
