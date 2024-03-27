from tasks import get_dates_of_publish_from_page


# def get_links_to_printed_form(soup):
#     divs_with_links = soup.findAll('div', class_='w-space-nowrap ml-auto registry-entry__header-top__icon')
#     links_to_printed_form = ['https://zakupki.gov.ru'+div.findAll('a')[1]['href'] for div in divs_with_links]
#     for number in range(0, len(links_to_printed_form)):
#         split_link = links_to_printed_form[number].split('.html')
#         split_link.insert(1,'Xml.html')
#         final_link = ''.join(split_link)
#         links_to_printed_form[number] = final_link
#     return links_to_printed_form

# def get_date_of_publication(links_to_printed_form):
#     pass



# def get_dates_of_publish_from_page(page_number):
#     url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
#     params = {
#         'fz44': 'on',
#         'pageNumber': page_number
#     }
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     soup = bs(response.text, 'lxml')
#     get_links_to_printed_form(soup)

    # print(response.url)
    # print(response.text)

# get_dates_of_publish_from_page(1)
def main():
    get_dates_of_publish_from_page.delay(1)
    get_dates_of_publish_from_page.delay(2)

if __name__=='__main__':
    main()