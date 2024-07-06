import requests
from bs4 import BeautifulSoup
import pandas as pd

Product_name = []
Prices = []
Description = []
Reviews = []

for i in range(2, 11):
    # Base URL for Flipkart search
    url = 'https://www.flipkart.com/search?q=phone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=' + str(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    # This will help to find the particular div only not the entire page
    box = soup.find("div", class_='DOjaWF gdgoEp')

    if box:
        names = box.find_all("div", class_='KzDlHZ')
        for name in names:
            Product_name.append(name.text)
        
        prices = box.find_all('div', class_='Nx9bqj _4b5DiR')
        for price in prices:
            Prices.append(price.text)
        
        desc = box.find_all("ul", class_='G4BRas')
        for d in desc:
            Description.append(d.text)
        
        reviews = box.find_all("div", class_='XQDdHH')
        for review in reviews:
            Reviews.append(review.text)

# To handle the issue where lists are of different lengths,
# ensure all lists have the same length by filling with default values

max_length = max(len(Product_name), len(Prices), len(Description), len(Reviews))

Product_name += [''] * (max_length - len(Product_name))
Prices += [''] * (max_length - len(Prices))
Description += [''] * (max_length - len(Description))
Reviews += [''] * (max_length - len(Reviews))

df = pd.DataFrame({
    'Product Name': Product_name,
    'Prices': Prices,
    'Description': Description,
    'Reviews': Reviews
})

# Save to CSV file
output_path = "flipkart_mobiles.csv"
df.to_csv(output_path, index=False)

print("Data saved to", output_path)
