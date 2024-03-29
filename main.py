from time import sleep

from tasks import get_links_to_xml_from_page, get_dates
from celery import chord


def main():
    links_to_printed_form = get_links_to_xml_from_page.delay(1)
    links_to_printed_form2 = get_links_to_xml_from_page.delay(2)

    new_test = links_to_printed_form.get()
    for link in new_test:
        get_dates.delay(link)

    new_test2 = links_to_printed_form2.get()
    for link2 in new_test2:
        get_dates.delay(link2)


if __name__ == '__main__':
    main()
