import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import threading

# Selenium WebDriver setup
def create_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (optional)
    chrome_options.add_argument("--disable-gpu")
    chrome_service = ChromeService(executable_path="path_to_chromedriver")  # Update path to chromedriver
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

# Function to open the URL in Selenium browser
def open_url_in_browser(url):
    try:
        driver = create_webdriver()
        driver.get(url)
        title = driver.title
        messagebox.showinfo("Page Loaded", f"Page Title: {title}")
        driver.quit()
    except WebDriverException as e:
        messagebox.showerror("Error", f"Could not load page: {str(e)}")

# Run Selenium in a separate thread
def run_in_thread(url):
    threading.Thread(target=open_url_in_browser, args=(url,), daemon=True).start()

# Tkinter GUI setup
def create_gui():
    def on_open_url():
        url = url_entry.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a URL.")
            return
        run_in_thread(url)

    # Create the main window
    root = tk.Tk()
    root.title("Tkinter + Selenium App")

    # URL Input
    tk.Label(root, text="Enter URL:").grid(row=0, column=0, padx=10, pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=10)

    # Open URL Button
    open_url_button = tk.Button(root, text="Open URL", command=on_open_url)
    open_url_button.grid(row=1, column=0, columnspan=2, pady=10)

    # Start the Tkinter main loop
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
