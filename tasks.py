import logging
import xml
from time import sleep

import requests
from bs4 import BeautifulSoup as bs
from celery import Celery
import xmltodict


celery = Celery(__name__,
                broker='redis://172.21.0.2:6379/0',
                backend='redis://172.21.0.2:6379/0')


def get_links_to_printed_form(soup):
    divs_with_links = soup.findAll('div', class_='w-space-nowrap ml-auto registry-entry__header-top__icon')
    links_to_printed_form = ['https://zakupki.gov.ru'+div.findAll('a')[1]['href'] for div in divs_with_links]
    for number in range(0, len(links_to_printed_form)):
        split_link = links_to_printed_form[number].split('.html')
        split_link.insert(1,'Xml.html')
        final_link = ''.join(split_link)
        links_to_printed_form[number] = final_link
    return links_to_printed_form


@celery.task(name="get_dates")
def get_dates(link):
    try:
        response = requests.get(link)
        # print(link)
        dict_data = xmltodict.parse(response.content)
        main_key = list(dict_data.keys())[0]
        date = dict_data[main_key]['commonInfo']['publishDTInEIS']
        return link, date
    except xml.parsers.expat.ExpatError:
        logging.error(f'Несовпадающий тег, пробую заново')
        sleep(1)
        get_dates(link)


@celery.task(name="get_dates_of_publish_from_page")
def get_dates_of_publish_from_page(page_number):
    try:
        url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
        params = {
            'fz44': 'on',
            'pageNumber': page_number
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        soup = bs(response.text, 'lxml')
        links_to_printed_form = get_links_to_printed_form(soup)
        for link in links_to_printed_form:
            get_dates.delay(link)
    except requests.exceptions.HTTPError:
        logging.error(f'Ошибка http-подключения к серверу, переподключаюсь')
        sleep(2)
        get_dates_of_publish_from_page(page_number)

