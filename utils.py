
def get_links_to_printed_form(soup):
    divs_with_links = soup.findAll('div', class_='w-space-nowrap ml-auto registry-entry__header-top__icon')
    links_to_printed_form = ['https://zakupki.gov.ru'+div.findAll('a')[1]['href'] for div in divs_with_links]
    for number in range(0, len(links_to_printed_form)):
        split_link = links_to_printed_form[number].split('.html')
        split_link.insert(1,'Xml.html')
        final_link = ''.join(split_link)
        links_to_printed_form[number] = final_link
    return links_to_printed_form

