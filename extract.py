import requests
from bs4 import BeautifulSoup
import csv

product_page_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

page = requests.get(product_page_url)

soup = BeautifulSoup(page.content, 'html.parser')

all_table_data = soup.find_all('td')

universal_product_code = all_table_data[0].get_text()
title = soup.find('h1').get_text()
price_including_tax = all_table_data[2].get_text()
price_excluding_tax = all_table_data[3].get_text()
number_available = all_table_data[5].get_text()
product_description = soup.find(id='product_description').find_next_sibling().get_text()
category = soup.find(class_='active').find_previous_sibling().get_text().strip()
review_rating = soup.find(class_='star-rating')['class'][1]
image_url = "http://books.toscrape.com/" + soup.find('img')['src'].split('../../')[1]

en_tete = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax",
            "number_available", "product_description", "category", "review_rating", "image_url"]

with open("books_data.csv", "w") as output_csv_file:
    writer = csv.writer(output_csv_file, delimiter=',')
    writer.writerow(en_tete)
    writer.writerow([product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                     number_available, product_description, category, review_rating, image_url])