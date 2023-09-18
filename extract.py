import requests
from bs4 import BeautifulSoup
import csv

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
        
def extract_book_data(book_page_soup):
    all_table_data = book_page_soup.find_all('td')

    universal_product_code = all_table_data[0].get_text()
    title = book_page_soup.find('h1').get_text()
    price_including_tax = all_table_data[2].get_text()
    price_excluding_tax = all_table_data[3].get_text()
    number_available = all_table_data[5].get_text()[10:-1].split()[0]
    product_description = book_page_soup.find(id='product_description').find_next_sibling().get_text()
    category = book_page_soup.find(class_='active').find_previous_sibling().get_text().strip()
    review_rating = get_numeric_rating(book_page_soup.find(class_='star-rating')['class'][1])
    image_url = "http://books.toscrape.com/" + book_page_soup.find('img')['src'].split('../../')[1]

    return [universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]

def get_page_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def extract_all_page_books_data(category_page_soup):
    all_page_books_soup = category_page_soup.find_all(class_="product_pod")
    all_page_books_data = []
    for book in all_page_books_soup:
        book_page_url = "http://books.toscrape.com/catalogue/" + book.find('a')['href'].split('../../../')[1]
        book_page = requests.get(book_page_url)
        book_page_soup = BeautifulSoup(book_page.content, 'html.parser')
        all_page_books_data.append([book_page_url] + extract_book_data(book_page_soup))
    return all_page_books_data

def get_next_page_url(page_soup):
    try:
        next_page = page_soup.find(class_="next").findChild('a')['href']
    except AttributeError:
        return False
    return "http://books.toscrape.com/catalogue/category/books/" + category + "/" + next_page

category = "mystery_3"
category_page_url = "http://books.toscrape.com/catalogue/category/books/" + category + "/index.html"
category_page_soup = get_page_soup(category_page_url)

en_tete = ["product_page_url", "universal_ product_code (upc)", "title", "price_including_tax", "price_excluding_tax",
            "number_available", "product_description", "category", "review_rating", "image_url"]

with open("category_books_data.csv", "w") as output_csv_file:
    writer = csv.writer(output_csv_file, delimiter=',')
    writer.writerow(en_tete)
    all_category_books_data = []
    all_category_books_data += extract_all_page_books_data(category_page_soup)
    
    next_page_url = get_next_page_url(category_page_soup)
    while(next_page_url):
        category_page_url = next_page_url
        category_page_soup = get_page_soup(category_page_url)
        all_category_books_data += extract_all_page_books_data(category_page_soup)
        next_page_url = get_next_page_url(category_page_soup)

    for book_data in all_category_books_data:
        writer.writerow(book_data)