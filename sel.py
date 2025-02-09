import pandas as pd


# /opt/anaconda3/bin/python sel.py
# Import statements
from selenium import webdriver  # Main Se


# lenium package for browser automation
# Manages ChromeDriver service
from selenium.webdriver.chrome.service import Service

# Chrome-specific configuration options
from selenium.webdriver.chrome.options import Options

# Provides locator strategies (ID, CLASS, etc.)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Implements explicit waits

# Conditions for WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # For adding delays between actions

# Function to set up the Chrome WebDriver


def setup_driver():
    chrome_options = Options()  # Create a new Options object for Chrome
    service = Service()  # Create a new Service object to manage ChromeDriver
    # Initialize Chrome with our settings
    return webdriver.Chrome(service=service, options=chrome_options)


# Function to log in to the application
def login(driver, username, password):
    driver.get('http://127.0.0.1:5500/frontend/login.html')

    wait = WebDriverWait(driver, 10)  # Set up a WebDriverWait with a timeout of 10 seconds
    # Find the username and password fields
    username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
    # Enter the provided username and password
    time.sleep(2)
    username_field.send_keys(username)
    time.sleep(2)
    password_field.send_keys(password)
    time.sleep(2)
    # Find and click the login button
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Login"]')))
    login_button.click()
    time.sleep(2)


# Function to add a new game
def add_game(driver, title, genre, price, quantity):
    # Find the title, genre, price, and quantity fields
    wait = WebDriverWait(driver, 10)  # Set up a WebDriverWait with a timeout of 10 seconds
    title_field = wait.until(EC.presence_of_element_located((By.ID, 'game-title')))
    genre_field = wait.until(EC.presence_of_element_located((By.ID, 'game-genre')))
    price_field = wait.until(EC.presence_of_element_located((By.ID, 'game-price')))
    quantity_field = wait.until(EC.presence_of_element_located((By.ID, 'game-quantity')))
    # Enter the provided game information
    time.sleep(2)
    title_field.send_keys(title)
    time.sleep(2)
    genre_field.send_keys(genre)
    time.sleep(2)
    price_field.send_keys(price)
    time.sleep(2)
    quantity_field.send_keys(quantity)
    time.sleep(2)
    # Find and click the add game button
    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Add Game"]')))
    add_button.click()
    time.sleep(2)
    # click on the alert
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)


def add_user(driver, name, email, phone):
    # Find the name, email, and phone fields
    wait = WebDriverWait(driver, 10)  # Set up a WebDriverWait with a timeout of 10 seconds
    name_field = wait.until(EC.presence_of_element_located((By.ID, 'user-name')))
    email_field = wait.until(EC.presence_of_element_located((By.ID, 'user-email')))
    phone_field = wait.until(EC.presence_of_element_located((By.ID, 'user-phone')))
    # Enter the provided user information
    time.sleep(2)
    name_field.send_keys(name)
    time.sleep(2)
    email_field.send_keys(email)
    time.sleep(2)
    phone_field.send_keys(phone)
    time.sleep(2)
    # Find and click the add user button
    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Add User"]')))
    add_button.click()
    time.sleep(2)
    # click on the alert
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)


# Function to add games from an Excel sheet
def add_games_from_excel(driver, file_path):
    df = pd.read_excel(file_path)
    login(driver, 'admin', 'admin123')
    for _, row in df.iterrows():
        add_game(driver, row['Title'], row['Genre'], row['Price ($)'], row['Quantity'])

def add_users_from_excel(driver, file_path):
    df = pd.read_excel(file_path)
    login(driver, 'admin', 'admin123')
    for _, row in df.iterrows():
        add_user(driver, row['Full Name'], row['Email'], row['Phone Number'])

if __name__ == "__main__":
    driver = setup_driver()
    time.sleep(5)
    try:
        # add_games_from_excel(driver, 'video_games_inventory.xlsx')
        add_users_from_excel(driver, 'users_list.xlsx')
    finally:
        driver.quit()


