import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

sponsored_texts = [
    "Sponsored",
    "Promotional content",
    "Paid partnership",
    "Được tài trợ",
    "Capcut",
]


def init_selenium(driver_path, run_with_debug):
    # Set Chrome options to use the debugging port
    chrome_options = Options()
    if run_with_debug:
        chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

    # Set up your WebDriver with the Service class (make sure the path is correct for your setup)
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open TikTok's discover page or hashtag page
    driver.get("https://www.tiktok.com")

    # Give time for the page to load
    time.sleep(5)

    # Create ActionChains instance for scrolling
    actions = ActionChains(driver)
    return driver


def scroll_tiktok(driver, num_videos=10):
    # Locate the body tag for scrolling
    body = driver.find_element(By.TAG_NAME, 'body')
    un_sponsored_articles = []
    filename = create_file_name()
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    for i in range(num_videos):
        un_sponsored_article = remove_non_sponsor(driver, filename)
        if un_sponsored_article:
            un_sponsored_articles.append(un_sponsored_article)
        # Scroll down (this simulates pressing the "Page Down" key)
        body.send_keys(Keys.ARROW_DOWN)

        # Wait to let video load and play a bit
        time.sleep(5)

        if (i + 1) % 5 == 0 and i > 0:
            for un_sponsored_article in un_sponsored_articles:
                driver.execute_script("arguments[0].remove();", un_sponsored_article)
            un_sponsored_articles = []

    print("Scrolling complete.")


def remove_non_sponsor(driver, filename):
    try:
        video = driver.find_element(By.TAG_NAME, 'video')
        article = video.find_element(By.XPATH, './ancestor::article[1]')
        if any(sponsored_text.lower() in article.text.lower() for sponsored_text in sponsored_texts):
            f = open(filename, "a", encoding="utf-8", errors="ignore")
            video_url = video.get_attribute("src")
            if not video_url:
                source = video.find_element(By.TAG_NAME, "source")
                video_url = source.get_attribute("src")
            f.write("------------------------------\n")
            f.write("Content: \n")
            f.write(article.text)
            f.write("\n")
            f.write("Video url: ")
            f.write(video_url)
            f.write("\n")
            f.write("------------------------------\n")
            f.close()
            return None
        return article
    except Exception as e:
        return None


def create_file_name():
    # Get current date and time
    now = datetime.now()

    # Format the date and time as a string
    return now.strftime("file_%Y-%m-%d_%H-%M-%S.txt")


max_videos = int(input("Max videos: "))
driver_path = input("Chrome driver path: ")
driver_path = driver_path if driver_path else 'chromedriver.exe'
driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), driver_path)
print("driver path: " + driver_path)
sponsored_texts_input = input("Sponsored Text(Separate by comma; example ): Được tài trợ,Capcut ")
if sponsored_texts_input:
    sponsored_texts = sponsored_texts_input.split(",")
# init driver
run_with_debug = input("Run with debug: ")
run_with_debug = True if run_with_debug.lower() == 'y' else False

driver = init_selenium(driver_path, run_with_debug)

start = input("Start: type Y/y: ")
if start.lower() == 'y':
    # Run the scroll function
    max_videos = max_videos if max_videos else 10
    scroll_tiktok(driver, max_videos)

    # Close the browser
    driver.quit()

# /usr/bin/google-chrome-stable --remote-debugging-port=9222 --no-first-run --no-default-browser-check --user-data-dir=remote-profile
# 130.0.6723.91
