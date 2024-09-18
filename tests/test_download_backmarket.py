import pytest
from src.download_backmarket_urls import Download_URLS
from src.download_url_elements import Download_Elements
from src.download_products import Download_Products


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

    @pytest.fixture
    def de(self):
        return Download_Elements()

    def test_soup_fetching(self, de):
        soup_list = de.fetch_soup_via_content()
        print(soup_list)

        assert soup_list is not None

    
    def test_soup_saving(self, de):
        filename = 'soup_data'
        max_age = 3 #days

        soup_data = de.verify_soup_data_age(filename, max_age)
        print(soup_data)

        assert soup_data is not None

    
    def test_element_fetching(self, de):
        filename = 'soup_data'
        max_age = 3 #days

        soup_data = de.verify_soup_data_age(filename, max_age)

        element_data = de.extend_elements_via_soup_data(soup_data)
        print(element_data)

        assert element_data is not None

    
    def test_element_saving(self, de):
        max_age = 3 #days
        
        soup_filename = 'soup_data'
        element_filename = 'element_data'

        soup_data = de.verify_soup_data_age(soup_filename, max_age)
        if soup_data:
            element_data = de.verify_element_data_age(element_filename, max_age, soup_data)
            print(element_data)

        assert element_data is not None

#########################
# TESTING PRODUCT CLASS #
#########################

    @pytest.fixture
    def dp(self):
        return Download_Products()

    
    def test_price_title_fetching(self, dp):
        product_specifics = dp.fetch_product_specifics()
        print(product_specifics)

        assert product_specifics is not None

    @pytest.mark.selected
    def test_specifics_saving(self, dp):
        product_specifics = dp.save_product_specifics()
        print(product_specifics)

        assert product_specifics is not None