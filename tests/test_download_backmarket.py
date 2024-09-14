import pytest
from src.download_backmarket_urls import Download_URLS
# from src.download_url_elements import Download_Elements


class TestDownloadBackmarketUrls:

    @pytest.fixture
    def du(self):
        return Download_URLS()

    def test_fetch_main_page_element(self, du):
        main_page = "https://www.backmarket.com/en-us"
        main_element = du.fetch_main_page_element(main_page)
        assert main_element is not None

    def test_store_href_addresses(self, du):
        main_element = ""  # Need to mock this main element
        assert du.store_href_addresses(main_element) is not None

    def test_stored_urls():
        # tester method for retrieving url data from the backmarket homepage
        main_page = "https://www.backmarket.com/en-us"
        download = Download_URLS(url=main_page)
        main_element = download.fetch_main_page_element()
        print(download.store_href_addresses())
        assert main_element is not None

    def test_url_saving(self, du):
            filename = "url_data"
            max_age = 3  # Maximum days that the code can be used up until the next refresh

            url_data = du.verify_data_age(filename, max_age)
            print(url_data)
            assert url_data is not None

#########################
# TESTING ELEMENT CLASS #
#########################

    def de(self):
        return Download_Elements()

    @pytest.mark.selected
    def test_soup_fetching(self, de):
        soup_list = de.fetch_soup_via_content()
        print(soup_list)

        assert soup_list is not None

