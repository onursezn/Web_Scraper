from bs4 import BeautifulSoup
import requests
import copy
from time import sleep
from random import randint
import time
from IPython.display import clear_output


'''
This programs glances through the pages of books list and grabs urls for each book.
input: www.idefix.com/Kategory/Edebiyat/page=1
    it can check till page=n
output: www.idefix.com/book1, www.idefix.com/book2, www.idefix.com/book3 ...
'''

site_page_nos= [str(i) for i in range(2,1407)] #1407 total page no
number_of_requests_from_site = 0
href_list = []              #list for book Urls
start_time = time.time()
page_no_max = []            #to learn until which page the program runs if exits unexpectedly

try:
    for site_page_no in site_page_nos:
        try:
            response = requests.get('https://www.idefix.com/kategori/Kitap/Edebiyat/grupno=00055')
            assert response.status_code == 200

            # to trace the program on terminal window
            number_of_requests_from_site += 1
            current_time = time.time()
            elapsed_time = current_time - start_time
            print('Request: {}; Frequency: {} requests/s'.format(number_of_requests_from_site, number_of_requests_from_site/elapsed_time))
            clear_output(wait=True)

            soup = BeautifulSoup(response.text, 'html.parser')

            divler = soup.find_all('div', attrs={'style':'height: 55px;'})

            page_no_max.append(site_page_no)

            for div in divler:
                a = div.find('a')
                #creating an url for a book
                href_list.append('https://www.idefix.com'+ a['href'])

            sleep(randint(2, 4))

        except Exception as e:
            print(e)
            pass

    href_list_copy = copy.deepcopy(href_list)

except Exception as e:
    print(e)

finally:
    #writing book urls to txt file for book_detail_url_for_idefix.py
    with open('DATABASE/Kategori-Edebiyat/Sayfalar-2_1207/edebiyat_kategori_urls_for_books.txt', 'w') as file:
        for href in href_list_copy:
            file.write(href + '\n')

    #txt file to see until which page the program is runned
    with open('DATABASE/Kategori-Edebiyat/Sayfalar-2_1207/until_which_page_runned.txt', 'w') as file:
        for page_no in page_no_max:
            file.write(page_no + '\n')

href_list_copy = copy.deepcopy(href_list)

