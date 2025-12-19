# Import the necessary modules
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import booking.constants as const
from booking.booking_filtration import BookingFilter

# Create a new class for booking
class Booking(webdriver.Edge):
    def __init__(self, teardown=False):
        self.teardown = teardown # Controls whether to quit the browser on exit
        # Initialize the Edge WebDriver
        super(Booking, self).__init__()
        self.maximize_window()

    def __exit__(self, *_):
        # Quit the WebDriver session
        if self.teardown:
            self.quit()

    def land_first_page(self):
        # Navigate to the booking website's homepage
        self.get(const.URL)
    
    def close_login_popup(self):
        try:
            login_popup = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Ignorar información sobre el inicio de sesión."]'))
            )
            login_popup.click()
        except:
            pass

    def change_currency(self, currency=0, code='USD'):
        # Open the currency picker
        currency_button = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'))
        )
        currency_button.click()

        # Wait for the currency list
        currency_items = WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[data-testid="selection-item"] span[class*="Picker_selection-text"]'))
        )
        # Click by index
        currency_items[currency].click() # Default is American Dollar

        # Validate the currency change
        selected_currency = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"] span[class*="ca2ca5203b"]'))
        )
        if selected_currency.text != code:
            raise Exception(f'Currency did not change to {code}') # Default is USD
        
    def destination_field(self, city='Guadalajara'):
        # Wait for the form and enter destination
        destination = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.NAME, 'ss'))
        )
        destination.clear()
        destination.send_keys(city) # Default is Guadalajara Jalisco, México
        
        # Validate the input
        if destination.get_attribute('value') != city:
            raise Exception(f'Destination input failed, expected {city}')
        
        # Wait for the dropdown to update and select the first option of the city
        destination_results = WebDriverWait(self, 10).until(
            lambda driver: driver.find_element(By.CSS_SELECTOR, 'ul[role="group"] li[id="autocomplete-result-0"]')

            if driver.find_element(By.CSS_SELECTOR, 'ul[role="group"] li[id="autocomplete-result-0"]').text.startswith(city)
            
            else False
        )
        destination_results.click()

    def pick_dates(self, checkin_date, checkout_date):

        # Wait for the date picker to be visible
        calendar = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="searchbox-datepicker"]'))
        )

        # Select check-in date
        self.find_element(By.CSS_SELECTOR, f'td[role="gridcell"] span[data-date="{checkin_date}"]').click()

        # Select check-out date
        self.find_element(By.CSS_SELECTOR, f'td[role="gridcell"] span[data-date="{checkout_date}"]').click()

    def occupancy(self, adults=3, children=0, rooms=2):
        # Click on the occupancy button
        self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]').click()

        # Wait for the occupancy modal to appear
        occupancy_modal = WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'e484bb5b7a'))
        )

        # Decrease adults to 1 before setting desired number
        while True:
            decrease_adults_button = occupancy_modal[0].find_elements(By.CSS_SELECTOR, 'button.de576f5064')[0]
            decrease_adults_button.click()

            adults_value = occupancy_modal[0].find_element(By.CLASS_NAME, 'e32aa465fd')
            
            if int(adults_value.text) == 1:
                break

        # Set adults
        adults_button = occupancy_modal[0].find_element(By.CSS_SELECTOR, 'button[class="de576f5064 b46cd7aad7 e26a59bb37 c295306d66 c7a901b0e7 aaf9b6e287 dc8366caa6"]')
        for _ in range(adults - 1):
            adults_button.click() # Default is 3 adults.
        
        # Set children
        children_button = occupancy_modal[1].find_element(By.CSS_SELECTOR, 'button[class="de576f5064 b46cd7aad7 e26a59bb37 c295306d66 c7a901b0e7 aaf9b6e287 dc8366caa6"]')
        for _ in range(children):
            children_button.click() # Default is 0 children
        
        # Set rooms
        rooms_button = occupancy_modal[2].find_element(By.CSS_SELECTOR, 'button[class="de576f5064 b46cd7aad7 e26a59bb37 c295306d66 c7a901b0e7 aaf9b6e287 dc8366caa6"]')
        for _ in range(rooms - 1):  
            rooms_button.click() # Default is 2 rooms.
        
        # Validate occupancy selection
        occupancy_button_label = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]').get_attribute('aria-label')

        if occupancy_button_label != f'Número de personas y de habitaciones. Selección actual: {adults} adultos · {children} niños · {rooms} habitaciones':
            raise Exception('Occupancy selection did not update correctly')
        
    def search(self):
        # Click the search button
        self.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Validate that the search results page has loaded
        search_results = WebDriverWait(self, 10).until(
            EC.url_contains('searchresults')
        )
        if not search_results:
            raise Exception('Search failed')

    # Filter results    
    def apply_filters(self):
        filtration = BookingFilter(driver=self)
        filtration.filter_by_star(3, 4)
        filtration.filter_by_lowest_price()