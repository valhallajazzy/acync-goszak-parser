from tasks import get_links_to_xml_from_page, get_dates, dynamic_map


def main():
    get_links_to_xml_from_page.apply_async((1,), link=dynamic_map.s(callback=get_dates))
    get_links_to_xml_from_page.apply_async((2,), link=dynamic_map.s(callback=get_dates))


if __name__ == '__main__':
    main()
