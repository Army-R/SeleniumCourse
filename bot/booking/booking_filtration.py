# Import necessary modules
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Class with methods to filter booking search results

class BookingFilter:
    def __init__(self, driver):
        self.driver = driver
    
    def filter_by_star(self, *stars):
        # Wait for the star ratings filter section to load
        star_ratings = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-filters-group="class"]'))
        )
        # Find and click the desired star rating checkbox
        star_ratings_options = star_ratings.find_element(By.CSS_SELECTOR, 'div[data-testid="filters-group-container"]')
        for star in stars:
            for star_rating in star_ratings_options.find_elements(By.TAG_NAME, 'input'):
                if str(star_rating.get_attribute('value')).strip() == f'class={star}':
                    star_rating.click()
                else:
                    continue

    def filter_by_lowest_price(self):
        # Find and click on the dropdown at the top
        filter_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]'))
        )
        filter_dropdown.click()

        # Find and click lowest price option
        low_price_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-id="price"]'))
        )
        low_price_option.click()

        # Validate filter was applied
        price_result = WebDriverWait(self.driver, 10).until(
            EC.url_contains('order=price')
        )
        if not price_result:
            raise Exception('Price filter application failed')