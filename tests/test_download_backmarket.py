import pytest
from src.download_backmarket_urls import Download_URLS
from src.download_url_elements import Download_Elements
from src.download_products import Download_Products
from src.eBay_urls import eBay_URLS
from src.eBay_elements import eBay_Elements


class TestDownloadBackmarketUrls:

    @pytest.fixture
    def du(self):
        return Download_URLS()
    
    
    def test_backmarket_element(self, du):
        element_data = du.fetch_main_page_element()
        print(element_data)

        assert element_data is not None

    
    def test_href_addresses(self, du):
        main_element = du.fetch_main_page_element()
        href_addresses = du.store_href_addresses(main_element)
        print(href_addresses)

        assert href_addresses is not None

    def test_url_saving(self, du):
        url_data = du.save_url_data()
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
        soup_data = de.save_soup_data()
        print(soup_data)

        assert soup_data is not None

    
    def test_element_fetching(self, de):
        soup_data = de.verify_soup_data_age(filename, max_age)

        element_data = de.extend_elements_via_soup_data(soup_data)
        print(element_data)

        assert element_data is not None

    
    def test_element_saving(self, de):
        element_data = de.save_element_data()
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

    
    def test_specifics_saving(self, dp):
        product_specifics = dp.save_product_specifics()
        print(product_specifics)

        assert product_specifics is not None
    
#####################
# TESTING URL CLASS #
#####################

    @pytest.fixture
    def eu(self):
        return eBay_URLS()

    
    def test_url_fetching(self, eu):
        eBay_URLS = eu.fetch_all_urls()
        print(eBay_URLS)

        assert eBay_URLS is not None
    
    
    def test_eBay_url_saving(self, eu):
        eBay_urls = eu.save_eBay_url_data()
        print(eBay_urls)

        assert eBay_urls is not None
    
######################
# TEST ELEMENT CLASS #
######################
    @pytest.fixture
    def ee(self):
        return eBay_Elements()

    
    def test_eBay_soup_fetching(self, ee):
        eBay_soups = ee.fetch_all_soups()
        print(eBay_soups)

        assert eBay_soups is not None

    @pytest.mark.selected
    def test_eBay_soup_saving(self, ee):
        eBay_soups = ee.save_eBay_soup_data()
        print(eBay_soups)

        assert eBay_soups is not None