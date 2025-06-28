from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open LeetCode problemset page
driver.get("https://leetcode.com/problemset/all/")

# Scroll to load problems
SCROLL_PAUSE_TIME = 1.2
MAX_PROBLEMS = 2500
print("Scrolling to load up to 2500 problems...")

problem_links = set()
last_height = driver.execute_script("return document.body.scrollHeight")

for _ in range(100):  # Max scroll attempts
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

    cards = driver.find_elements(By.CLASS_NAME, "group")
    for card in cards:
        href = card.get_attribute("href")
        if href and "/problems/" in href:
            slug = href.split("/problems/")[1].split("/")[0]
            clean_url = f"https://leetcode.com/problems/{slug}"
            problem_links.add(clean_url)

    print(f"Problems collected: {len(problem_links)}")

    if len(problem_links) >= MAX_PROBLEMS:
        print("Collected 2500 problems. Stopping scroll.")
        break

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print("No more content to load.")
        break
    last_height = new_height

# Save to lc.txt
with open("lc.txt", "w", encoding="utf-8") as f:
    for link in sorted(problem_links)[:MAX_PROBLEMS]:
        f.write(link + "\n")

driver.quit()
print(f"\nDone! Total unique problems saved in lc.txt: {min(len(problem_links), MAX_PROBLEMS)}")