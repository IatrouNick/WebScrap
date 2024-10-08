import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Function to get HTML content of a webpage
def get_page_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Function to scrape product information from one page
def scrape_ebay_products(soup):
    products = []
    for item in soup.select('.s-item'):
        name = item.select_one('.s-item__title').text if item.select_one('.s-item__title') else None
        price = item.select_one('.s-item__price').text if item.select_one('.s-item__price') else None
        condition = item.select_one('.SECONDARY_INFO').text if item.select_one('.SECONDARY_INFO') else None
        shipping = item.select_one('.s-item__shipping').text if item.select_one('.s-item__shipping') else "Free shipping"
        
        if name and price:
            products.append({
                'Name': name,
                'Price': price,
                'Condition': condition,
                'Shipping': shipping
            })
    return products

# Function to handle pagination and scrape multiple pages
def scrape_multiple_pages_ebay(search_query, pages=3):
    all_products = []
    base_url = "https://www.ebay.com/sch/i.html?_nkw="
    query_url = f"{base_url}{search_query.replace(' ', '+')}"

    for page in range(1, pages + 1):
        url = f"{query_url}&_pgn={page}"
        print(f"Scraping page {page}: {url}")
        page_content = get_page_content(url)
        
        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            products = scrape_ebay_products(soup)
            all_products.extend(products)
        
        # Adding a delay between requests to avoid getting blocked
        time.sleep(random.uniform(2, 5))
    
    return all_products

# Function to save data to CSV
def save_to_csv(products, filename="ebay_products.csv"):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Example usage
if __name__ == "__main__":
    search_query = "laptops"  # Change the search term as needed
    product_data = scrape_multiple_pages_ebay(search_query, pages=4)
    save_to_csv(product_data)
