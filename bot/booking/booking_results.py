# import necessary modules
from selenium.webdriver.common.by import By

# Loop through the results and display them
class BookingResults:
    def __init__(self, hotels):
        self.hotels = hotels

    def loop_through_results(self): 
        for result in self.hotels[:10]:  # Limiting to first 10 results for brevity
            
            hotel_name = result.find_element(
                By.CSS_SELECTOR, 
                'div[data-testid="title"]'
            ).text
            
            hotel_price = result.find_element(
                By.CSS_SELECTOR, 
                'span[data-testid="price-and-discounted-price"]'
            ).text
        
            print(f'Hotel: {hotel_name} - Price: {hotel_price}')    