import selenium
from selenium.common import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import config
import time

chrome_driver_path = "C:/Users/Quinn/Development/chromedriver.exe"
URL = "https://tinder.com/"

driver = selenium.webdriver.Chrome(service=Service(executable_path=chrome_driver_path))
driver.get(url=URL)


def click_next_element(xpath):
    try:
        element = WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
    except AttributeError or StaleElementReferenceException or NoSuchElementException or TimeoutException:
        click_next_element(xpath)


# 0. accept cookies
click_next_element('//*[@id="t897152800"]/div/div[2]/div/div/div[1]/div[1]/button')

# 1. log in
click_next_element('//*[@id="t897152800"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a')

# 2. log in with facebook
click_next_element('//*[@id="t-831228276"]/div/div/div[1]/div/div/div[3]/span/div[2]/button')

# 3.1 Refocus driver to facebook login window
WebDriverWait(driver, 5).until(ec.number_of_windows_to_be(2))
driver.switch_to.window(driver.window_handles[-1])

# 3.2 fill in email and password fields
email_field = driver.find_element(By.NAME, "email")
password_field = driver.find_element(By.NAME, "pass")
email_field.send_keys(config.facebook_email)
password_field.send_keys(config.facebook_pass, Keys.ENTER)

# 3.3 Switch back to tinder window
WebDriverWait(driver, 5).until(ec.number_of_windows_to_be(1))
driver.switch_to.window(driver.window_handles[-1])

# 4. allow location tracking
click_next_element('//*[@id="t-831228276"]/div/div/div/div/div[3]/button[1]')

# 5. disable notifications
click_next_element('//*[@id="t-831228276"]/div/div/div/div/div[3]/button[2]')

# 6. "Swipe no" until there are no more swipes available
# Trying to get Selenium to find the fucking swipe left button because it's shitting the bed on the xpath...
buttons = driver.find_elements(By.CSS_SELECTOR, "button.button")
for button in buttons:
    if button.text == "NOPE":
        swipe_left = button
    print(button.text)

for x in range(100):
    time.sleep(1)
    try:
        print("trying to swipe left...")
        swipe_left.click()
    except ElementClickInterceptedException:
        click_next_element('//*[@id="t-831228276"]/div/div/div[2]/button[2]')
