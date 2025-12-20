# Import necessary modules
from booking.booking import Booking

with Booking(teardown=True) as bot:
    bot.land_first_page()
    bot.close_login_popup()
    bot.change_currency() 
    bot.destination_field(input('Where are you going to? '))
    bot.pick_dates(
        checkin_date=input('Enter check-in date (YYYY-MM-DD): '), 
        checkout_date=input('Enter check-out date (YYYY-MM-DD): ')
    )
    bot.occupancy(
        adults=int(input('Number of adults: ')), 
        rooms=int(input('Number of rooms: '))
    ) 
    bot.search() 
    bot.apply_filters()
    bot.display_results()


if __name__ == '__main__':
    pass    