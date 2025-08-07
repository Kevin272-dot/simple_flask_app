from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Setup Chrome service
service = Service(
    'C:\\Users\\lrkev\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Open Google
driver.get('https://www.google.com')

# Wait for the page to load
time.sleep(2)

# Accept cookies if needed (Google may show a consent screen in some regions)
try:
    accept_button = driver.find_element(By.XPATH, "//div[text()='Accept all']")
    accept_button.click()
    time.sleep(1)
except:
    pass  # Skip if not shown

# Find the correct search input box
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('Selenium automation')
search_box.send_keys(Keys.RETURN)

# Wait for results to load (optional)
time.sleep(5)

# Close the browser
driver.quit()
