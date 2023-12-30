import os
import requests
from bs4 import BeautifulSoup

from constants import BASE_URL, CATALOGUE_URL, EXTRACTED_DATA_DIR


class WebPage:
    def __init__(self, url) -> None:
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self):
        response = requests.get(self.url)
        return BeautifulSoup(response.content, 'html.parser')


class Category(WebPage):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.name = self.soup.h1.string
        self.dir = EXTRACTED_DATA_DIR + self.name + '/'
        os.makedirs(self.dir, exist_ok=True)
        self.last_page = False
        self.books = []
    
    def find_next_page(self):
        try:
            next_page_url = self.soup.find(class_="next").a.get("href")
            self.url = self.url.rsplit('/', 1)[0] + '/' + next_page_url
            self.soup = super().get_soup()
        except AttributeError:
            self.last_page = True
    
    def extract_books_data(self):
        while not self.last_page:
            books_soups = self.soup.find_all(class_="product_pod")
            for book_soup in books_soups:
                book = Book(CATALOGUE_URL + book_soup.find('a').get("href").strip("../../../"), self)
                self.books.append(book)
            self.find_next_page()


class Book(WebPage):
    def __init__(self, url: str, category: Category) -> None:
        super().__init__(url)
        self.title = self.soup.h1.string
        self.category = category.name
        self.upc = self.soup.find("th", string="UPC").find_next_sibling().string
        self.price_excl_tax = self.soup.find("th", string="Price (excl. tax)").find_next_sibling().string
        self.price_incl_tax = self.soup.find("th", string="Price (incl. tax)").find_next_sibling().string
        self.availability = self.soup.find("th", string="Availability").find_next_sibling().string
        self.rating = self.soup.find(class_="star-rating").get("class")[1]
        self.image_url = BASE_URL + self.soup.img.get("src").strip("../../")
        try:
            self.description = self.soup.find(id="product_description").find_next_sibling().string
        except AttributeError:
            self.description = "No description found"
        self.download_image(category.dir)

    def download_image(self, category_dir):
        image = requests.get(self.image_url).content
        image_name = self.image_url.rsplit('/', 1)[1]
        with open(category_dir + image_name, "wb") as book_image_file:
            book_image_file.write(image)
    
    def get_data_for_csv(self):
        return [
            self.title,
            self.category,
            self.upc,
            self.price_excl_tax,
            self.price_incl_tax, 
            self.availability,
            self.rating,
            self.url,
            self.image_url,
            self.description,
        ]
