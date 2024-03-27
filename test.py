import logging
import xml
from time import sleep

import xmltodict
import requests

def leg():
    try:
        url = 'https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0338300047924000061'
        response = requests.get(url)
        dict_data = xmltodict.parse(response.content)
        main_key = list(dict_data.keys())[0]
        date = dict_data[main_key]['commonInfo']['publishDTInEIS']
        print(url, ' - ', date)
    except xml.parsers.expat.ExpatError:
        logging.error(f'Несовпадающий тег, пробую заново')
        sleep(1)

leg()