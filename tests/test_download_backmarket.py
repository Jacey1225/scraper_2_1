import pytest
from src.download_backmarket_urls import Download_URLS
from src.download_url_elements import Download_Elements
from src.download_products import Download_Products
from src.eBay_urls import eBay_URLS
from src.eBay_elements import eBay_Elements
from src.eBay_products import eBay_Products
from src.database_conversion import Convert_Data


class TestDownloadBackmarketUrls:

    @pytest.fixture
    def bu(self):
        return Download_URLS()
    
    
    def test_backmarket_urls(self, bu):
        backmarket_urls = bu.save_url_data()
        print(backmarket_urls)

        assert backmarket_urls is not None

####################
# TEST SOUP SAVING #
####################

    @pytest.fixture
    def be(self):
        return Download_Elements()
    
    
    def test_backmarket_soups(self, be):
        backmarket_soups = be.save_soup_data()
        assert backmarket_soups is not None

#######################
# TEST PRODUCT SAVING #
#######################

    @pytest.fixture
    def pd(self):
        return Download_Products()
    
    def test_product_data_saving(self, pd):
        product_data = pd.save_product_data()
        print(product_data)

        assert product_data is not None

########################
# TEST EBAY URL SAVING #
########################

    @pytest.fixture
    def eud(self):
        return eBay_URLS()

    
    def test_ebay_url_saving(self, eud):
        eBay_url_data = eud.save_eBay_url_data()
        print(eBay_url_data)

        assert eBay_url_data is not None

###########################
# TEST PRODUCT ATTRIBUTES #
###########################
    @pytest.fixture
    def pad(self):
        return eBay_Products()
    
    
    def test_product_attributes(self, pad):
        product_attributes = pad.save_attributes_data()
        print(product_attributes)

        assert product_attributes is not None
    
############################
# TEST DATABASE CONVERSION #
############################

    @pytest.fixture
    def dc(self):
        return Convert_Data()
    
    @pytest.mark.selected
    def test_data_conversion(self, dc):
        database = dc.transform_collection()
        if database is not None:
            print('database converted')
        

    

