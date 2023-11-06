#<<<<<<< HEAD

import requests
from bs4 import BeautifulSoup
import csv
import os

url = "http://books.toscrape.com/catalogue/1st-to-die-womens-murder-club-1_2/index.html"
def extract_book_data(book_url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    body = soup.find('body')

    table = soup.find(class_="table table-striped")
    universal_product_code = table.select('td')[0].get_text(strip = True)
    price_including_tax = table.select("td")[3].get_text(strip = True)
    price_excluding_tax = table.select("td")[2].get_text(strip = True)
    quantity_available = table.select("td")[5].get_text(strip = True)
    review_rating = table.select("td")[6].get_text(strip = True)
    category = body.find('ul', {'class':'breadcrumb'}).select('li')[2].find('a').get_text(strip = True)
    product_description = soup.select("p")[3].get_text(strip = True)
    book_title = soup.select('h1')[0].text
    image_url = body.find('img').get('src').replace('../../', 'http://books.toscrape.com/')

    book_data = {'book_url': book_url, 'universal_product_code': universal_product_code, 'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax, 'quantity_available': quantity_available,'review_rating': review_rating, 'category': category, 'product_description': product_description, 'book_title': book_title, 'image_url': image_url}

    headers = ["product_page_url", "universal_product_code(upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]
    headers_content = {'product_page_url': url, 'universal_product_code(upc)': universal_product_code, 'book_title': book_title, 'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax, 'quantity_available': quantity_available, 'product_description': product_description, 'category': category, 'review_rating': review_rating, 'image_url': image_url}

    if os.path.isfile("books_online.csv"):
        with open("books_online.csv", "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writerow(headers_content)
    else:
        with open("books_online.csv","w",newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerow(headers_content)


    return book_data

extract_book_data(url)


def extract_book_category_url(category_url):
    for i in range(1, 3):
        categoryURL = 'http://books.toscrape.com/catalogue/category/books/mystery_3/page-' + str(i) + '.html'
        result = requests.get(categoryURL)
        #print(categoryURL)

        soup = BeautifulSoup(result.content, 'html.parser')

        category_book_url_list = soup.find_all('h3')

        for url_links in category_book_url_list:
            book_urls = (url_links.find('a').get('href').replace('../../..', 'http://books.toscrape.com/catalogue'))
            print(book_urls)

    book_url_list = {'category_url': book_urls}


    return book_url_list

categoryURL = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
extract_book_category_url(categoryURL)





#>>>>>>> origin/master
