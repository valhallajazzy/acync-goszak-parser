import xml

from utils import get_links_to_printed_form
from tasks import get_dates
from contextlib import nullcontext as does_not_raise
import pytest
from bs4 import BeautifulSoup as bs


class TestUtils:
    @pytest.mark.parametrize(
        "soup, res, expectation",
        [
            (bs('<div></div>', 'lxml'), [], does_not_raise()),
            (None, None, pytest.raises(AttributeError)),
            ([], None, pytest.raises(AttributeError)),
            ('a', None, pytest.raises(AttributeError)),
        ]
    )
    def test_get_links_to_xml_from_page(self, soup, res, expectation):
        with expectation:
            assert get_links_to_printed_form(soup) == res


class TestTasks:
    @pytest.mark.parametrize(
        "link, res, expectation",
        [
            ('https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0322200005224000086',
             ('https://zakupki.gov.ru/epz/order/notice/printForm/viewXml.html?regNumber=0322200005224000086',
              '2024-03-22T10:58:36.364+10:00'), does_not_raise()
             ),
            ('https://abc.com', None, pytest.raises(xml.parsers.expat.ExpatError)),
        ]
    )
    def test_get_dates(self, link, res, expectation):
        with expectation:
            assert get_dates(link) == res



