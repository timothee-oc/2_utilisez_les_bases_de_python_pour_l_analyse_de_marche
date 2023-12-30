import requests
from constants import BASE_URL, CATALOGUE_URL
from bs4 import BeautifulSoup

def download_image(category_dir, book_image_url):
    book_image = requests.get(book_image_url).content
    book_image_name = book_image_url.rsplit('/', 1)[1]
    with open(category_dir + book_image_name, "wb") as book_image_file:
        book_image_file.write(book_image)

def extract_category_books_data(category_soup):
        category_books_data = []
        category_books_soups = category_soup.find_all(class_="product_pod")
        for category_book_soup in category_books_soups:
            category_book_url = CATALOGUE_URL + category_book_soup.find('a').get("href").strip("../../../")
            book_soup = get_soup(category_book_url)
            book_title = book_soup.h1.string
            book_rating = book_soup.find(class_="star-rating").get("class")[1]
            book_image_url = BASE_URL + book_soup.img.get("src").strip("../../")
            book_description = book_soup.find(id="product_description")
            if book_description:
                book_description = book_description.find_next_sibling().string
            book_upc = book_soup.find("th", string="UPC").find_next_sibling().string
            book_price_excl_tax = book_soup.find("th", string="Price (excl. tax)").find_next_sibling().string
            book_price_incl_tax = book_soup.find("th", string="Price (incl. tax)").find_next_sibling().string
            book_availability = book_soup.find("th", string="Availability").find_next_sibling().string
            category_books_data.append([
                book_title,
                book_description,
                book_upc,
                book_price_excl_tax,
                book_price_incl_tax,
                book_availability,
                book_rating,
                category_book_url,
                book_image_url,
            ])
        return category_books_data

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')