# OpenclassroomsProject:  Books to Scrape

## **Description**
#### Project to create Books Online price monitoring system that extracts book data on Books to Scrape: http://books.toscrape.com/.
#### The following book details extraction required: product_page_url, universal_ product_code (upc), book_title, price_including_tax, price_excluding_tax, quantity_available, product_description, category, review_rating, and image_url.

## **How to run the code?**
### ● Clone the repository (Windows and macOS)
### ● In the terminal, navigate to your project folder

### ● Create a virtual environment by running the command:
  _Python3 – m venv env (Windows and macOS)_  

### ● Activate the virtual environment by running the command:
_env\Scripts\activate.bat (Windows),
env/bin/activate (macOS)_

### ● Install Python library:
_pip install -r requirement.txt (Windows and macOS)_
### ● Import packages:
    - import requests
    - from bs4 import BeautifulSoup
    - import csv
    - import os.path
    - import shutil

### ● Run the program

##### The program will extract, transform, and load:
- All book genres on Books to Scrape
- Save to CSV file each category book detail and their downloaded book images
##### ***![Example of Mystery category’s CSV file](readme_image/Example_csvfile.png)***

- download and save book images
##### ***![Example of the Mystery category’s image](readme_image/Example_book_image.png)***
 

