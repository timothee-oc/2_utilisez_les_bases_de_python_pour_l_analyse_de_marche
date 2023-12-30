import os
import csv
from tqdm import tqdm

from functions import get_soup, extract_category_books_data, download_image
from constants import BASE_URL, EXTRACTED_DATA_DIR, BOOKS_DATA_FILE_NAME, HEADERS

home_soup = get_soup(BASE_URL)
side_categories_soup = home_soup.find(class_="side_categories")
categories_urls = [BASE_URL + a.get('href') for a in side_categories_soup.find_all('a')]

for category_url in tqdm(categories_urls[1:], desc="categories"):
    category_soup = get_soup(category_url)
    category_name = category_soup.h1.string
    category_dir = EXTRACTED_DATA_DIR + category_name + '/'
    os.makedirs(category_dir, exist_ok=True)

    with open(category_dir + BOOKS_DATA_FILE_NAME, 'w', encoding="utf-8") as books_data_file:
        csv_writer = csv.writer(books_data_file, delimiter=',')
        csv_writer.writerow(HEADERS) 
        last_page = False
        while not last_page:
            category_books_data = extract_category_books_data(category_soup)
            for book_data in category_books_data:
                book_data.insert(1, category_name)
                csv_writer.writerow(book_data)
                download_image(category_dir, book_data[-1])
            next_page_button = category_soup.find(class_="next")
            if next_page_button:
                next_url = category_url.rsplit('/', 1)[0] + '/' + next_page_button.a.get("href")
                category_soup = get_soup(next_url)
            else:
                last_page = True