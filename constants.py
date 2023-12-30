BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"
EXTRACTED_DATA_DIR = "extracted_data/"
HEADERS = [
    "TITLE",
    "CATEGORY",
    "DESCRIPTION",
    "UNIVERSAL PRODUCT CODE (UPC)",
    "PRICE (EXCL. TAX)",
    "PRICE (INCL. TAX)", 
    "AVAILABILITY",
    "RATING",
    "BOOK PAGE URL",
    "IMAGE URL"
]
BOOKS_DATA_FILE_NAME = "books_data.csv"