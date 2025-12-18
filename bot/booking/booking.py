# Import the necessary modules
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

    def change_currency(self, currency=0):
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
        currency_items[currency].click() # Default is USD