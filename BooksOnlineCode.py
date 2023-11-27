#<<<<<<< HEAD

import requests
from bs4 import BeautifulSoup
import csv
import os


url = "http://books.toscrape.com/"
category_url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'

#get_all_categories
def get_all_book_categories():
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    urls = []

    navigation_panel = soup.find('ul', {'class': 'nav nav-list'}).find('ul').select('a')

    for category in navigation_panel:
        category_url = url + category.get('href')
        category_name = category.get_text(strip = True)
        urls.append(category_url)

    return urls

all_urls = get_all_book_categories()
print(all_urls)

get_all_book_categories()


#get category book urls
def get_category_book_url(category_url):
    books_in_category = []
    book_links = category_url

    while book_links != None:
        response = requests.get(book_links)
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('body')

        next_page = soup.find('li', {'class': 'next'})

        articles = body.findAll('h3')
        for link in articles:
            book_url = link.find('a').get('href').replace('../../../', str(url) + 'catalogue/').replace('../../', str(url) + 'catalogue/')
            books_in_category.append(book_url)

        if next_page != None:
            next_page_element = next_page.find('a').get('href')
            book_links = category_url.replace('index.html', str(next_page_element))

        else:
            book_links == None
            break

    return books_in_category

links = get_category_book_url(category_url)
print(links)

get_category_book_url(category_url)


#extract product data for one category
#book_url = 'http://books.toscrape.com/catalogue/in-a-dark-dark-wood_963/index.html'

def get_book_data(book_url):

    books = []
    links = get_category_book_url(category_url)
    book_url = links

    for b in book_url:
        books.append(b)
        
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find('body')

    table = soup.find(class_="table table-striped")
    universal_product_code = table.select('td')[0].get_text(strip=True)
    price_including_tax = table.select("td")[3].get_text(strip=True)
    price_excluding_tax = table.select("td")[2].get_text(strip=True)
    quantity_available = table.select("td")[5].get_text(strip=True)
    review_rating = table.select("td")[6].get_text(strip=True)
    category = body.find('ul', {'class': 'breadcrumb'}).select('li')[2].find('a').get_text(strip=True)
    product_description = soup.select("p")[3].get_text(strip=True)
    book_title = soup.select('h1')[0].text
    image_url = body.find('img').get('src').replace('../../', 'http://books.toscrape.com/')

    book_data = {'book_url': book_url, 'universal_product_code': universal_product_code,
                 'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax,
                 'quantity_available': quantity_available, 'review_rating': review_rating, 'category': category,
                 'product_description': product_description, 'book_title': book_title, 'image_url': image_url}

    headers = ["product_page_url", "universal_product_code(upc)", "book_title", "price_including_tax",
               "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating",
               "image_url"]
    headers_content = {'product_page_url': url, 'universal_product_code(upc)': universal_product_code,
                       'book_title': book_title, 'price_including_tax': price_including_tax,
                       'price_excluding_tax': price_excluding_tax, 'quantity_available': quantity_available,
                       'product_description': product_description, 'category': category, 'review_rating': review_rating,
                       'image_url': image_url}

    if os.path.isfile("online_book_data.csv"):
        with open("online_book_data.csv", "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writerow(headers_content)
    else:
        with open("online_book_data.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerow(headers_content)


    return book_data


get_book_data(book_url)



"""
#get product data for one book
url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"
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

    with open("online_book_data.csv","w",newline="") as csvfile:
        headers = ["product_page_url", "universal_product_code(upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(csvfile, headers)
        writer.writeheader()
        writer.writerow({'product_page_url': url, 'universal_product_code(upc)': universal_product_code, 'book_title': book_title, 'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax, 'quantity_available': quantity_available, 'product_description': product_description, 'category': category, 'review_rating': review_rating, 'image_url': image_url})

    return book_data

extract_book_data(url)
"""




