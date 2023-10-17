import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content,'html.parser')
book_title = soup.find("h1")
table = soup.find(class_="table table-striped")
universal_product_code = table.select('td')[0].get_text(strip = True)
price_including_tax = table.select("td")[3].get_text(strip = True)
price_excluding_tax = table.select("td")[2].get_text(strip = True)
quantity_available = table.select("td")[5].get_text(strip = True)
category = soup.find(href="../category/books/mystery_3/index.html").get_text(strip = True)
product_description = soup.find("h2")
review_rating = table.select("td")[6].get_text(strip = True)
for image in soup.find_all('img'):
    print(image['src'])

image_url = image['src']
print(url)
print(universal_product_code)
print(book_title.get_text(strip=True))
print(price_including_tax)
print(price_excluding_tax)
print(quantity_available)
print(product_description.get_text(strip = True))
print(category)
print(review_rating)
print(image_url)



import csv

with open("books_online.csv","w",newline="") as csvfile:
    headers = ["product_page_url", "universal_product_code(upc)", "book_title", "price_including_tax", "price_excluding_tax", "quantity_available", "product_description", "category", "review_rating", "image_url"]
    writer = csv.DictWriter(csvfile, headers)
    writer.writeheader()
    writer.writerow({'product_page_url': url, 'universal_product_code(upc)': universal_product_code, 'book_title': book_title, 'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax, 'quantity_available': quantity_available, 'product_description': product_description, 'category': category, 'review_rating': review_rating, 'image_url': image_url})





