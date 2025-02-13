import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

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


# Current NIS to USD conversion rate (as of 2024)
NIS_TO_USD_RATE = 0.27  # 1 NIS = 0.27 USD

def convert_nis_to_usd(nis_price):
    """Convert price from NIS to USD"""
    return round(nis_price * NIS_TO_USD_RATE, 2)

def get_game_genre(game_url):
    """Fetch the genre from the game's individual page"""
    try:
        # Add a small delay to avoid overwhelming Steam's servers
        time.sleep(1)
        
        # Send GET request to the game page
        response = requests.get(game_url)
        if response.status_code != 200:
            return "Unknown"
        
        # Parse the game page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find genre information in the new structure
        genre_span = soup.find('span', {'data-panel': re.compile(r'{"flow-children":"row"}')} )
        if genre_span:
            # Find all genre links within the span
            genre_links = genre_span.find_all('a')
            # Get first genre (primary genre)
            if genre_links:
                # Extract just the genre name from the link text
                genre = genre_links[0].text.strip()
                return genre
        
        return "Unknown"
    except Exception as e:
        print(f"Error fetching genre: {str(e)}")
        return "Unknown"

def scrape_steam_games(limit=10):
    # URL of Steam's top sellers page
    url = 'https://store.steampowered.com/search/?filter=topsellers'
    
    # Send GET request
    response = requests.get(url)
    
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all games
    games = soup.find_all('a', {'class': 'search_result_row'})
    
    # List to store game data
    games_data = []
    
    print("Starting to scrape games...")
    
    # Limit the number of games to process
    for index, game in enumerate(games[:limit], 1):
        # Get game URL for fetching genre
        game_url = game['href']
        
        # Find the responsive name container
        name_container = game.find('div', {'class': 'responsive_search_name_combined'})
        if not name_container:
            continue
        
        # Extract title
        title_elem = name_container.find('span', {'class': 'title'})
        if not title_elem:
            continue
        title = title_elem.text
        
        print(f"Processing game {index}: {title}")
        
        # Get genre from game's page
        genre = get_game_genre(game_url)
        
        # Extract price
        price_elem = name_container.find('div', {'class': 'discount_final_price'})
        if not price_elem:
            price_elem = name_container.find('div', {'class': 'search_price'})
        
        # Initialize price
        price = 0  # Default to 0 for free games
        
        if price_elem:
            price_text = price_elem.text.strip().lower()
            if 'free' in price_text or 'free to play' in price_text:
                price = 0
            else:
                # Extract number from price text (e.g., "₪19.99" -> 19.99)
                price_match = re.search(r'₪?(\d+\.?\d*)', price_text)
                if price_match:
                    nis_price = float(price_match.group(1))
                    # Convert NIS to USD
                    price = convert_nis_to_usd(nis_price)
        
        # Default quantity for inventory
        quantity = 10
        
        # Add game data to list
        games_data.append({
            'Title': title,
            'Genre': genre,
            'Price ($)': price,
            'Quantity': quantity
        })
        
        print(f"Added {title} - {genre} - ${price:.2f}")
    
    return games_data

def create_games_excel(games_data, filename='video_games_inventory.xlsx'):
    # Create DataFrame
    df = pd.DataFrame(games_data)
    
    # Save to Excel
    df.to_excel(filename, index=False)
    print(f"Created Excel file: {filename}")
    return filename


def setup_driver():
    chrome_options = Options()  # Create a new Options object for Chrome
    service = Service()  # Create a new Service object to manage ChromeDriver
    # Initialize Chrome with our settings
    return webdriver.Chrome(service=service, options=chrome_options)


# Function to log in to the application
def login(driver, username, password):
    time.sleep(2)
    driver.get('http://127.0.0.1:5500/frontend/login.html')
    time.sleep(10)
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
    genre_field.send_keys(genre)
    price_field.send_keys(price)
    quantity_field.send_keys(quantity)
    # Find and click the add game button
    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Add Game"]')))
    add_button.click()
    time.sleep(1)
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
    try:
        print("Scraping games from Steam...")
        games_data = scrape_steam_games(limit=10)  # Limit to 10 games
        
        print(f"\nFound {len(games_data)} games")
        
        # Create Excel file
        excel_file = create_games_excel(games_data)
        
        print("Excel file created successfully!")
        add_games_from_excel(driver, 'video_games_inventory.xlsx')
        # add_users_from_excel(driver, 'users_list.xlsx')
    finally:
        driver.quit()


