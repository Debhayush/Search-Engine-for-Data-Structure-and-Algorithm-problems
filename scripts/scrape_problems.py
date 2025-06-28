import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup
LC_INPUT_FILE = "lc.txt"
OUTPUT_FOLDER = "problems"
TITLE_FILE = "problemtitles.txt"
URL_FILE = "problemurls.txt"

# Create folders
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
title_fp = open(TITLE_FILE, "w", encoding="utf-8")
url_fp = open(URL_FILE, "w", encoding="utf-8")

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 15)

# Read input URLs
with open(LC_INPUT_FILE, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

count = 1
for url in urls:
    print(f"\n Scraping ({count}): {url}")
    try:
        driver.get(url)
        time.sleep(2)

        try:
            # Get title from div.text-title-large > a
            title_element = wait.until(EC.presence_of_element_located((
                By.XPATH, '//div[contains(@class, "text-title-large")]//a'
            )))
            title = title_element.text.strip()

            # Get description body
            body_element = wait.until(EC.presence_of_element_located((
                By.CLASS_NAME, "elfjS"
            )))
            body = body_element.text.strip()

        except:
            print(" Skipping (likely premium or structure changed)")
            continue

        # Save data
        title_fp.write(title + "\n")
        url_fp.write(url + "\n")

        with open(os.path.join(OUTPUT_FOLDER, f"problemtext{count}.txt"), "w", encoding="utf-8") as pf:
            pf.write(body)

        print(f" Saved: {title}")
        count += 1

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Cleanup
title_fp.close()
url_fp.close()
driver.quit()
print(f"\n Finished scraping {count - 1} non-premium problems.")
