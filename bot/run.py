# Import necessary modules
from booking.booking import Booking

with Booking(teardown=True) as bot:
    bot.land_first_page()
    bot.close_login_popup()
    #bot.change_currency() 
    bot.destination_form()