import os
import sys

from bs4 import BeautifulSoup
import requests
import copy
import shutil
import re
from time import sleep
from random import randint, random
import pandas as pd
import time
from IPython.display import clear_output


flag_for_all_df = True

book_names = ''
author_list = []
publishers = ''
translators = ''
page_numbers = ''
isbns = ''
descriptions = ''
categories = []
urun_no_list = []
i = 10000           #if isbn doesnt exist give an incremental 'i's for isbn


all_df = pd.DataFrame({'book_name': [book_names],
                       'author': [author_list],
                       'publisher': [publishers],
                       'translator': [translators],
                       'page_number': [page_numbers],
                       'isbn': [isbns],
                       'description': [descriptions],
                       'category': [categories],
                       })

not_wanted_name_1 = 'Seti'
not_wanted_name_2 = 'Kitap-Takim'

start_time = time.time()
number_of_requests = 0

#read book urls
with open('DATABASE/Kategori-Edebiyat/Sayfalar-2_1207/edebiyat_kategori_urls_for_books-Copy.txt', 'r') as file:
    url_lists_for_each_book = file.readlines()

# read previously taken urunnolist
# with open('', 'r') as file:
#     urun_no_list = file.readlines()


try:
    '''getting a specific url for each book for detail view'''
    for url_for_book in url_lists_for_each_book[:12]:

        #'''not taking books which are named Seti, 5 Kitap Takım etc.'''
        if not_wanted_name_1 and not_wanted_name_2 in url_for_book:
            continue
        #'''not taking books which are not unique, and already in list'''
        elif url_for_book[-13:] in urun_no_list :
            continue

        urun_no_list.append(url_for_book[-13:])

        #headers = {'User-Agent': f'name (@email.com)'}
        response = requests.get(url_for_book[:-1])    # [:-1] slices the last \n so the url wll be accesible

        assert response.status_code == 200

        #to trace the program on terminal window
        number_of_requests += 1
        sleep(randint(0,3))
        current_time = time.time()
        elapsed_time = current_time - start_time
        print('Request #: {}; Frequency: {} requests/s'.format(number_of_requests, number_of_requests/elapsed_time))
        clear_output(wait = True)

        soup = BeautifulSoup(response.text, 'html.parser')


        #----------------ISBN
        try:
            isbn_number = soup.find("span", text=re.compile("Barkod:")).find_next().text.strip()

        except Exception as e:
            print(e)
            isbn_number = i         #if ISBN doesnt exist then give incrementing number
            i=i+1
        isbns = isbn_number
        isbn_code_for_image_name = copy.deepcopy(isbn_number)  #copied ISBN no for image file naming

        #----------------ISBN


        #----------------BOOK NAME
        try:
            book_name = soup.find("h1").string.strip()

            hasan = " - Hasan Ali Yücel Klasikleri"            #to delete book name's extra words
            if hasan in book_name:
                book_name = book_name[:-29]

        except Exception as e:
            print(e)
            book_name ='no book name'

        book_names = book_name

        #----------------BOOK NAME


        #----------------AUTHOR
        authors = []

        try:
            author_list = soup.find('span', text=re.compile('Yazar:')).find_next().find_all(href=re.compile("Yazar"))

            '''If there are several authors, it adds them to the list'''
            for a in author_list:
                authors.append(a.string.split(',')[0].strip())

        except Exception as e:
            print(e)
            authors = ['no author name']

        author_list = authors

        #----------------AUTHOR


        #----------------PUBLISHER

        try:
            publisher = soup.find(href=re.compile("Yayinevi")).string

        except Exception as e:
            print(e)
            publisher = 'no publisher'

        publishers = publisher

        #----------------PUBLISHER


        #----------------TRANSLATOR

        '''Checking whether the translator data exists for the URL'''
        try:
            translator = soup.find("span", text=re.compile("Çevirmen:")).find_next().get_text(strip=True)

        except AttributeError:
            translator = "No translator"

        translators = translator

        #----------------TRANSLATOR


        #----------------PAGE NUMBER

        '''Checking whether the page number data exists for the URL'''
        try:
            number_of_pages = soup.find("b", text=re.compile("Sayfa Sayısı:")).next_sibling.string.strip()

        except AttributeError:
            number_of_pages = "0"

        page_numbers = number_of_pages

        #----------------PAGE NUMBER


        #----------------DESCRIPTION

        try:
            description = soup.find("div", class_="product-description").text
        except Exception as e:
            print(e)
            description = 'no description'

        def description_stripper_for_idefix(desc):
            '''It splits the last part of description in case there are some irrevelant info'''
            splitters_list = ["En Sevilen Kitaplara Hemen Şimdi Sahip Olun!","(Tanıtım Bülteninden)",
                              "İnce Kapak:", "Ciltli:", "Sayfa Sayısı:", "Kitap Adı:", "e-Kitap" ]

            for i in range(len(splitters_list)):
                if splitters_list[i] in desc:
                    desc = desc.split(splitters_list[i])[0]
                    return desc.lstrip().rstrip()

        descriptions = description_stripper_for_idefix(description)

        #----------------DESCRIPTION


        #----------------CATEGORY

        '''check whether all categories are available'''
        try:
            all_categories = soup.find("ul", attrs={"class":"breadcrumb"}).find_all(href=re.compile("kategori"))

        except Exception as e:
            print(e)
            all_categories = 'no category'

        def category_lister(category):
            '''If available put all category types to the list.
                e.g. Edebiyat>Roman>Dünya  to ['Edebiyat', 'Roman', 'Dünya']
            '''

            category_list = []
            if category[1].string:
                category_1 = category[1].string
                category_list.append(category_1)
            try:
                category_2 = category[2].string
                category_list.append(category_2)
            except IndexError:
                category_2 = ''
            try:
                category_3 = category[3].string
                category_list.append(category_3)
            except IndexError:
                category_3 = ''
            try:
                category_4 = category[4].string
                category_list.append(category_4)
            except IndexError:
                category_4 = ''
            try:
                category_5 = category[5].string
                category_list.append(category_5)
            except IndexError:
                category_5 = ''

            return category_list

        categories = category_lister(all_categories)

        #----------------CATEGORY


        #----------------IMAGE
        '''Getting the cover image of the book'''
        try:
            image_ = soup.find('img', attrs={'id': 'main-product-img'})
            image_src = image_.get('data-src')

            image_url = image_src
            response_for_image = requests.get(image_url, stream=True)

            if response_for_image.status_code == 200:
                with open(f'C:\\Users\\sezen\\Desktop\\pycharm projects\\webscrap\\example\\DATABASE\\Kategori-Edebiyat\\Sayfalar-2_1207\\images\\{isbn_code_for_image_name}.jpg', 'wb') as f:
                    response_for_image.raw.decode_content = True
                    shutil.copyfileobj(response_for_image.raw, f)


        except Exception as e:
            print(e)
            pass
        #----------------IMAGE


        #Creating a DataFrame in each for loop(for each book)
        df = pd.DataFrame({'book_name': [book_names],
                           'author': [author_list],
                           'publisher': [publishers],
                           'translator': [translators],
                           'page_number': [page_numbers],
                           'isbn': [isbns],
                           'description': [descriptions],
                           'category': [categories],
                           })
        print("above request's url: " + url_for_book)

        #If its first time do not append so that first row wouldn't be 0
        if flag_for_all_df:
            all_df = df
            flag_for_all_df = False

        else:
            all_df = all_df.append(df, ignore_index=True)


except Exception as e:

    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

finally:

    #keeping the record of urun no list for future program runs so that the program wouldn't run if a book already exists
    with open('DATABASE/Kategori-Edebiyat/Sayfalar-2_1207/urun_no_list.txt', 'w') as file:
        file.writelines(urun_no_list)

    #Data Frame is created when program ends
    all_df.to_csv('DATABASE/Kategori-Edebiyat/Sayfalar-2_1207/book_detail_dataframe.csv', encoding='utf-16')

