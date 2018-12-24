# this script fetches data from 20 pages of the website 'https://www.ihome.ir'.
# then creates and stores data in SQL database.
import requests
from bs4 import BeautifulSoup
import mysql.connector
from unidecode import unidecode
# using timing.py to find out program's runtime
import timing

price_list = []
bedrooms_list = []
area_list = []


def find_price(input_soup):
    price = input_soup.find_all('div', class_='price', attrs={'data-price'})
    for i in range(1, len(price)):
        # using unidecode to convert persian numbers to english numbers
        pr = unidecode(price[i].text).replace('twmn', '')
        pr = pr.replace(',', '').strip()
        if pr.isdigit():
            price_list.append(int(pr))
        else:
            price_list.append('0')


def find_details(input_soup):
    bed = input_soup.find_all('ul', class_='left slider_pinfo')
    for i in bed:
        li = i.text.split()
        if len(li) == 11:
            del li[6:11]
        if len(li) == 9:
            del li[4:9]
        if len(li) == 6:
            bedrooms_list.append(int(unidecode(li[0])))
            area_list.append(int(unidecode(li[2]).replace(',', '')))
        elif len(li) == 4:
            bedrooms_list.append(0)
            area_list.append(int(unidecode(li[0]).replace(',', '')))
        elif len(li) == 2:
            bedrooms_list.append(int(unidecode(li[0])))
            area_list.append(0)
        elif len(li) == 0:
            bedrooms_list.append(0)
            area_list.append(0)


def scrape():
    web_page = 'https://www.ihome.ir/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86/%D8%AA%D9%87%D8%B1%D8%A7%D9%86/{}/'
    # here you can change the number of pages that you want to collect the data from
    # I used 25 pages which collects 600 data
    for page_number in range(1, 21):
        resp = requests.get(web_page.format(page_number))
        soup = BeautifulSoup(resp.text, 'html.parser')
        find_price(soup)
        find_details(soup)

def data_base():
    my_db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="19941994"
    )

    my_cursor = my_db.cursor()
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS ihome_website")
    my_cursor.execute('USE ihome_website')
    my_cursor.execute("CREATE TABLE IF NOT EXISTS home (bedroom INT , area INT , price BIGINT)")
    for i, j, k in zip(bedrooms_list, area_list, price_list):
        my_cursor.execute("INSERT INTO home VALUES ('{}','{}','{}')".format(i, j, k))
    my_db.commit()
    my_db.close()


if __name__ == '__main__':
    scrape()
    data_base()
