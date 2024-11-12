import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Define the URL of the website
url = "https://example.com/snacks"  # Replace with the actual URL

# User-Agent to simulate a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# Lists to hold data
product_names = []
prices = []
country_labels = []
num_reviews = []

# Make a request to the website
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check if request was successful
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the product listing section on the webpage
    product_elements = soup.find_all("div", class_="product-item")  # Adjust based on the actual class name
    
    # Loop through each product item and extract details
    for product in product_elements:
        # Product name
        name = product.find("h2", class_="product-title").get_text(strip=True)
        product_names.append(name)

        # Price
        price = product.find("span", class_="product-price").get_text(strip=True)
        prices.append(price)

        # Country label (if present)
        country = product.find("span", class_="country-label")
        if country:
            country_labels.append(country.get_text(strip=True))
        else:
            country_labels.append("N/A")

        # Number of reviews (if present)
        reviews = product.find("span", class_="review-count")
        if reviews:
            num_reviews.append(reviews.get_text(strip=True))
        else:
            num_reviews.append("0")

        # Optional: add a delay to avoid rapid-fire requests
        time.sleep(random.uniform(0.5, 2.0))

    # Create a DataFrame and save data
    data = pd.DataFrame({
        "Product Name": product_names,
        "Price": prices,
        "Country Label": country_labels,
        "Number of Reviews": num_reviews
    })

    # Save data to a CSV file
    data.to_csv("snack_products.csv", index=False)
    print("Data saved to snack_products.csv")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
