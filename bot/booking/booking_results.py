# import necessary modules
from selenium.webdriver.common.by import By

# Collect the results
class BookingResults:
    def __init__(self, hotels):
        self.hotels = hotels
    
    def loop_through_results(self):
        # Display the first 10 results  
        for result in self.hotels:
            
            hotel_name = result.find_element(
                By.CSS_SELECTOR, 
                'div[data-testid="title"]'
            ).text
            
            hotel_price = result.find_element(
                By.CSS_SELECTOR, 
                'span[data-testid="price-and-discounted-price"]'
            ).text
            
            return f'Hotel: {hotel_name} - Price: {hotel_price}'