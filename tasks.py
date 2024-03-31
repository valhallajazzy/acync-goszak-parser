import logging
import os
import xml
from utils import get_links_to_printed_form

import requests
from bs4 import BeautifulSoup as bs
from celery import Celery
import xmltodict
from dotenv import load_dotenv


load_dotenv()

celery = Celery(__name__,
                broker=os.getenv('CELERY_BROKER_URL'),
                backend=os.getenv('CELERY_RESULT_BACKEND'))

celery.conf.event_serializer = 'pickle'
celery.conf.task_serializer = 'pickle'
celery.conf.result_serializer = 'pickle'
celery.conf.accept_content = ['application/json', 'application/x-python-serialize']


@celery.task(name="get_dates", max_retries=3)
def get_dates(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            dict_data = xmltodict.parse(response.content)
            main_key = list(dict_data.keys())[0]
            date = dict_data[main_key]['commonInfo']['publishDTInEIS']
            return link, date
    except xml.parsers.expat.ExpatError as exc:
        logging.error(f'Несовпадающий тег, пробую заново')
        raise get_dates.retry(exc=exc, countdown=5)


@celery.task(name="get_links_to_xml_from_page", max_retries=3)
def get_links_to_xml_from_page(page_number):
    try:
        url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
        params = {
            'fz44': 'on',
            'pageNumber': page_number
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        soup = bs(response.text, 'lxml')
        print(soup)
        links_to_printed_form = get_links_to_printed_form(soup)
        return links_to_printed_form
    except requests.exceptions.HTTPError as exc:
        logging.error(f'Ошибка http-подключения к серверу, переподключаюсь')
        raise get_links_to_xml_from_page.retry(exc=exc, countdown=5)


@celery.task(name="dynamic_map")
def dynamic_map(links, callback):
    for link in links:
        callback.delay(link)

