import csv
from tqdm import tqdm

from constants import BASE_URL, BOOKS_DATA_FILE_NAME, HEADERS
from classes import Category

def main():
    all_category = Category(BASE_URL)
    side_categories_links = all_category.soup.find(class_="side_categories").find_all('a')[1:]
    for category_link in tqdm(side_categories_links, desc="categories"):
        category = Category(BASE_URL + category_link.get('href'))
        with open(category.dir + BOOKS_DATA_FILE_NAME, 'w', encoding="utf-8") as books_data_file:
            csv_writer = csv.writer(books_data_file, delimiter=',')
            csv_writer.writerow(HEADERS)
            category.extract_books_data()
            for book in category.books:
                csv_writer.writerow(book.get_data_for_csv())

if __name__ == '__main__':
    main()
