# Import necessary modules
from booking.booking import Booking

with Booking(teardown=True) as bot:
    bot.land_first_page()
    bot.close_login_popup()
    bot.change_currency() 
    bot.destination_field()
    bot.pick_dates('2025-12-21', '2026-01-12')
    bot.occupancy() 
    bot.search() 