# Import the necessary modules
from selenium import webdriver
import booking.constants as const

# Create a new class for booking
class Booking(webdriver.Edge):
    def __init__(self, teardown=False):
        self.teardown = teardown # Controls whether to quit the browser on exit
        # Initialize the Edge WebDriver
        super(Booking, self).__init__()
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Quit the WebDriver session
        if self.teardown:
            self.quit()

    def land_first_page(self):
        # Navigate to the booking website's homepage
        self.get(const.URL)