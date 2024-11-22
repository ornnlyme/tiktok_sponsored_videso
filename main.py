import os
import sys
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
    time.sleep(1)

    # Create ActionChains instance for scrolling
    actions = ActionChains(driver)
    return driver


def scroll_tiktok(driver, num_videos=10):
    try:
        # Locate the body tag for scrolling
        body = driver.find_element(By.TAG_NAME, 'body')
        current_index = 0

        while (True):
            articles = driver.find_elements(By.TAG_NAME, 'article')
            if current_index != len(articles):
                current_index = len(articles)
                time.sleep(1)
                articles[-1].click()
            # Scroll down (this simulates pressing the "Page Down" key)
            time.sleep(1)
            body.send_keys(Keys.ARROW_UP)
            body.send_keys(Keys.ARROW_DOWN)
            body.send_keys(Keys.ARROW_DOWN)

            # Wait to let video load and play a bit
            print(f"No of articles: {len(articles)}.")
            if len(articles) >= num_videos:
                break

        print("Scrolling complete.")
        print("Start removing non sponsor videos.")

        for article in articles:
            un_sponsored_article = remove_non_sponsor(article)
            if un_sponsored_article:
                driver.execute_script("arguments[0].remove();", un_sponsored_article)

        print("Removing non sponsor videos complete.")

        copy_video_url(driver)
    except Exception as e:
        print(f"Scroll tiktok failed: {e}")


def remove_non_sponsor(article):
    try:
        html = article.get_attribute("outerHTML")
        if any(sponsored_text.lower() in html.lower() for sponsored_text in sponsored_texts):
            return None
        return article
    except Exception as e:
        print(f"Remove non sponsor video failed: {e}")
        return None


def copy_video_url(driver):
    try:
        print("Write sponsor video url to file.")
        articles = driver.find_elements(By.TAG_NAME, 'article')
        if len(articles) == 0:
            return
        article = articles[0]
        article.click()
        comment = driver.find_element("xpath", "//span[@data-e2e='comment-icon']")
        comment.click()
        filename = create_file_name()
        exe_dir = get_executable_dir()
        filepath = os.path.join(exe_dir, filename)
        f = open(filepath, "a", encoding="utf-8", errors="ignore")
        for i in range(len(articles)):
            video_url = driver.current_url
            f.write("------------------------------\n")
            f.write(video_url)
            f.write("\n")
            down_button = driver.find_element("xpath", "//button[@data-e2e='arrow-right']")
            down_button.click()

        f.close()
        print("Write sponsor video url to file complete \n")
        print(f"File: {filepath}")
    except Exception as e:
        print(f"Copy video url failed: {e}")


def create_file_name():
    # Get current date and time
    now = datetime.now()

    # Format the date and time as a string
    return now.strftime("file_%Y-%m-%d_%H-%M-%S.txt")


def get_driver_path():
    if getattr(sys, 'frozen', False):  # If bundled by PyInstaller
        # Locate the driver in the bundled files
        return os.path.join(sys._MEIPASS, "chromedriver.exe")
    else:
        # For regular execution
        return "chromedriver.exe"

def get_executable_dir():
    if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller executable
        return os.path.dirname(sys.executable)  # Path to the .exe file
    else:
        return os.path.dirname(os.path.abspath(__file__))


driver_path = get_driver_path()
print("driver path: " + driver_path)
# init driver
# run_with_debug = input("Run with debug: ")
# run_with_debug = True if run_with_debug.lower() == 'y' else False

driver = init_selenium(driver_path, False)

start = input("Start: type Y/y: ")
if start.lower() == 'y':
    # Run the scroll function
    while True:
        sponsored_texts_input = input("Sponsored Text(Separate by comma; example ): Được tài trợ,Capcut ")
        if sponsored_texts_input:
            sponsored_texts = sponsored_texts_input.split(",")
        max_videos = int(input("Max videos: "))
        max_videos = max_videos if max_videos else 10
        scroll_tiktok(driver, max_videos)

        stop = input("Stop: type Y/y: ")
        if stop.lower() == 'y':
            # Close the browser
            driver.quit()
            break

# /usr/bin/google-chrome-stable --remote-debugging-port=9222 --no-first-run --no-default-browser-check --user-data-dir=remote-profile
# pyinstaller --onefile --add-data "chromedriver.exe;." main.py
# 130.0.6723.91
