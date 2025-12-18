# Import the necessary modules
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import booking.constants as const

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
        
    def destination_form(self, city='Guadalajara'):
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
        time.sleep(2) # Wait before clicking destination

        destination_results.click()

        time.sleep(2) # Wait before clikking on the date picker

        # Click on the date picker and Wait for the calendar to load
        date = WebDriverWait(self, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="searchbox-dates-container"]'))
        )
        date.click()

        calendar = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="searchbox-datepicker"]'))
        )