# Same program than on main branch but using OOP

# Instructions

* Install Python (version >= 3.11.5), and make sure pip is correctly installed alongside (version >= 23.2.1)
* Clone this repo in a local directory
* Create a virtual environment with the command : `py -m venv env`
* Enter this virtual environment with the command : `.\env\Scripts\activate`
* Install required python librairies from **requirements.txt** in your virtual environment with the command : `pip install -r requirements.txt`
* Execute the python script **extract.py** with the command : `py extract.py`

# Expected results

This script extract data from the website [Books to Scrape](http://books.toscrape.com/).
It creates a directory _extracted_data_ wich contains a sub-directory for each book category.
Each one of these sub-directories contains :
* A CSV file holding data of every book in the category, such as its title, its UPC code, its rating and much more !
* A JPG image file of the each book of the category.