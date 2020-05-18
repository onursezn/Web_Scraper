from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
import panda as pd
from warnings import warnwarn("Warning Simulation")
from time import timestart_time = time()
from IPython.core.display import clear_output
start_time = time()requests = 0

#requests = 0
#for _ in range(5):
# A request would go here
#    requests += 1
#    sleep(randint(1,3))
#    current_time = time()
#    elapsed_time = current_time - start_time
#    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
#clear_output(wait = True)

URL = "https://www.kitapyurdu.com/kitap/kar/311001.html"
#headers = {'User-Agent': f'Your name (your@email.com)'}
response = requests.get(URL)

assert response.status_code == 200

soup = BeautifulSoup(response.text, 'html.parser')

div = soup.find('div', attrs={'class': 'product-info'})

book_name = div.find('h1', attrs={'class': 'product-heading'}).string

author = div.find('div', attrs={'class':'manufacturers'}).find('span', attrs={'itemprop':'name'}).string.strip()

publisher = div.find('div', attrs={'class':'publishers'}).find('span', attrs={'itemprop':'name'}).string

description = div.find('div', attrs={'id':'description_text'}).find('span', attrs={'itemprop':'description'}).text

publishing_date = div.find('table', attrs={'class':'attribute'}).find('td', attrs={'itemprop':'datePublished'}).text

edition_number = div.find('table', attrs={'class':'attribute'}).find('span', attrs={'itemprop':'bookEdition'}).string

number_of_pages = div.find('table', attrs={'class':'attribute'}).find('span', attrs={'itemprop':'numberOfPages'}).string

isbn_number = div.find('table', attrs={'class':'attribute'}).find('span', attrs={'itemprop':'isbn'}).string

print(' ')
print('ISBN: ' + isbn_number)
print('book_name: ' + book_name)
print('author: ' + author)
print('publisher: ' + publisher)
print('description: ' + description)
print('publishing_date: ' + publishing_date)
print('edition_number: ' + edition_number)
print('number_of_pages: ' + number_of_pages)
