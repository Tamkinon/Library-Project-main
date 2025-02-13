import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

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

def main():
    try:
        print("Scraping games from Steam...")
        games_data = scrape_steam_games(limit=10)  # Limit to 10 games
        
        print(f"\nFound {len(games_data)} games")
        
        # Create Excel file
        excel_file = create_games_excel(games_data)
        
        print("Excel file created successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()