#<<<<<<< HEAD

import requests
from bs4 import BeautifulSoup
import csv
import os.path
import shutil

url = "http://books.toscrape.com/"


#get_all_categories
def get_all_book_categories():
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    urls = []

    navigation_panel = soup.find('ul', {'class': 'nav nav-list'}).find('ul').select('a')

    for category in navigation_panel:
        category_url = url + category.get('href')
        urls.append(category_url)

    return urls

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


#extract product data for each book
def get_book_data(book_url):

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

    book_data = {
        "product_page_url": book_url,
        "universal_product_code": universal_product_code,
        "book_title": book_title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "quantity_available": quantity_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url
    }

    headers = ["product_page_url", "universal_product_code(upc)", "book_title", "price_including_tax",
               "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating",
               "image_url"]
    headers_content = {"product_page_url": book_url, "universal_product_code(upc)": universal_product_code,
                       "book_title": book_title, "price_including_tax": price_including_tax,
                       "price_excluding_tax": price_excluding_tax, "quantity_available": quantity_available,
                       "product_description": product_description, "category": category, "review_rating": review_rating,
                       "image_url": image_url}

    folder = str(category)
    image_name = str(book_title) + "_" + "book_image.jpg"
    valid_image_name = image_name[:60].replace(':', "_").replace('#', '').replace('/','-').replace('\'', '').replace('\"', '').replace(',', '-').replace('é', 'e').replace('*','i').replace('?',"")

    if not os.path.exists(folder):
        os.makedirs(category)

    result = requests.get(image_url, stream=True)
    with open(os.path.join(folder, valid_image_name), 'wb') as f:
        shutil.copyfileobj(result.raw, f)

    return book_data


def main():
    category_urls = get_all_book_categories()

    for category_url in category_urls:
        book_urls = get_category_book_url(category_url)
        all_books_data = []
        for book_url in book_urls:
            book_detail = get_book_data(book_url)
            all_books_data.append(book_detail)

            category_name = category_url.split("/")[-2].split("_")[0].replace('-', " ")
            file_name = str(category_name) + "_" + "online_book_data.csv"
            header = all_books_data[0].keys()
            with open(f'{os.path.join(category_name, file_name)}.csv','w', encoding='utf-8', newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                writer.writerows(all_books_data)


main()

