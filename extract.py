import requests
from bs4 import BeautifulSoup
import csv
import re
import os
from tqdm import tqdm

def get_numeric_rating(review_rating):
    match review_rating:
        case "One":
            return "1"
        case "Two":
            return "2"
        case "Three":
            return "3"
        case "Four":
            return "4"
        case "Five":
            return "5"

def format_image_file_name(title):
    title_without_punctuation = re.sub(r'[^\w\s]', '', title)
    image_file_name = '_'.join(title_without_punctuation.lower().split())
    return image_file_name
    
def download_book_image(image_url, title):
    image_file_name = format_image_file_name(title)
    image_data = requests.get(image_url).content
    with open(images_dir_path + image_file_name + '.jpg', 'wb') as output_image_file:
        output_image_file.write(image_data)

def extract_book_data(book_page_soup):
    title = book_page_soup.find('h1').get_text()
    category = book_page_soup.find(class_='active').find_previous_sibling().get_text().strip()
    review_rating = get_numeric_rating(book_page_soup.find(class_='star-rating')['class'][1])
    image_url = base_url + book_page_soup.find('img')['src']
    try:
        product_description = book_page_soup.find(id='product_description').find_next_sibling().get_text()
    except AttributeError:
        product_description = "Aucune description"

    all_table_data = book_page_soup.find_all('td')

    universal_product_code = all_table_data[0].get_text()
    price_including_tax = all_table_data[2].get_text()
    price_excluding_tax = all_table_data[3].get_text()
    number_available = re.sub(r'[^\d]', '', all_table_data[5].get_text())
    
    download_book_image(image_url, title)

    return [universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]

def get_page_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def extract_all_page_books_data(category_page_soup):
    all_page_books_soup = category_page_soup.find_all(class_="product_pod")
    all_page_books_data = []
    for book in all_page_books_soup:
        book_page_url = category_base_url + book.find('a')['href']
        book_page_soup = get_page_soup(book_page_url)
        all_page_books_data.append([book_page_url] + extract_book_data(book_page_soup))
    return all_page_books_data

def get_next_page_url(page_soup):
    try:
        next_page = page_soup.find(class_="next").findChild('a')['href']
    except AttributeError:
        return None
    return category_base_url + next_page

def get_all_categories_indexes(page_soup):
    all_categories_indexes = []
    for a in page_soup.find(class_="side_categories").find_all('a')[1:]:
        all_categories_indexes.append(base_url + a['href'])
    return all_categories_indexes

base_url = "http://books.toscrape.com/"
home_page_soup = get_page_soup(base_url + "index.html")
all_categories_indexes = get_all_categories_indexes(home_page_soup)

en_tete = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax", 
           "number_available", "product_description", "category", "review_rating", "image_url"]

for category_index in tqdm(all_categories_indexes, desc="categories"):
    category_base_url = category_index.replace("index.html", '')
    category_name = category_index.split('/')[-2].split('_')[0].replace('-', '_')

    csv_data_dir_path = "all_extracted_data/" + category_name + "/csv_data/"
    images_dir_path = "all_extracted_data/" + category_name + "/images/"
    os.makedirs(csv_data_dir_path, exist_ok=True)
    os.makedirs(images_dir_path, exist_ok=True)

    with open(csv_data_dir_path + category_name + "_books_data.csv", "w", encoding="utf-8") as output_csv_file:
        writer = csv.writer(output_csv_file, delimiter=',')
        writer.writerow(en_tete)
        category_page_soup = get_page_soup(category_index)
        all_category_books_data = extract_all_page_books_data(category_page_soup)
        
        next_page_url = get_next_page_url(category_page_soup)
        while(next_page_url):
            category_page_soup = get_page_soup(next_page_url)
            all_category_books_data += extract_all_page_books_data(category_page_soup)

            next_page_url = get_next_page_url(category_page_soup)

        for book_data in all_category_books_data:
            writer.writerow(book_data)