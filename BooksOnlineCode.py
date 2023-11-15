#<<<<<<< HEAD

import requests
from bs4 import BeautifulSoup
import csv
import os

"""
url = "http://books.toscrape.com/catalogue/a-spys-devotion-the-regency-spies-of-london-1_3/index.html"
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

    if os.path.isfile("categories_books_online.csv"):
        with open("categories_books_online.csv", "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writerow(headers_content)
    else:
        with open("categories_books_online.csv","w",newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerow(headers_content)

    return book_data

extract_book_data(url)
for book_url in books_urls:
    book_data = extract_book_data(book_url)
"""

def extract_category_url(website_url):
    result = requests.get(website_url)
    soup = BeautifulSoup(result.content, 'html.parser')

    book_categories = soup.find("div", class_="side_categories").find_all("a")
    for category in book_categories:
        name = (category.get_text(strip = True))
        link = category["href"]
        categoryURLs = (website_url.replace('index.html','')+link)
        return categoryURLs
        #print(name,'',categoryURLs)

website_url = 'http://books.toscrape.com/index.html'
extract_category_url(website_url)

def get_books_url_by_category(category_url):
    result = requests.get(category_url)
    soup = BeautifulSoup(result.content, 'html.parser')

    while True:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        footer_element = soup.select_one('li.current')
        #print(footer_element.text.strip())

        next_page_element = soup.select_one('li.next > a')

        category_book_url_list = soup.find_all('h3')
        for url_links in category_book_url_list:
            book_urls = (url_links.find('a').get('href').replace('../..', 'http://books.toscrape.com/catalogue'))
            print(book_urls)
            if next_page_element:
                next_page_url = next_page_element.get('href')
            else:
                break


category_url = extract_category_url(website_url)
get_books_url_by_category(category_url)



#>>>>>>> origin/master
