from storage_dude import filter_films, execute_film_picking
from mubilifier import execute_main
from delivery_guy import content_generator, send_to_email
from datetime import date

# chose a directory to store the first 30 films extracted # ## MUST BE CSV ##
temp_data = 
# chose a directory to store the main database # ## MUST BE CSV ##
main_data = 

def get_new_films():
	# chose the days freely, MUBI.com/showing updates everyday #
	if date.today().strftime('%d') == '12' or date.today().strftime('%d') == '26':
		execute_main(temp_data)
		filter_films(main_data, temp_data)
	else:
		return 'No New Films to be added'

def send_film_of_the_week(bot_email, bot_passwd, your_email):
	# chose dates to send the film of the week #
	if date.today().strftime('%a') == 'Fri' or date.today().strftime('%a') == 'Mon':
		film_of_the_week = execute_film_picking(main_data)
		email_draft = content_generator(film_of_the_week)
		send_to_email(bot_email, bot_passwd, your_email, email_draft)
	else:
		'Film of the Week sent every MONDAY & FRIDAY'

# sender email #
bot_email = 
# sender password #
bot_passwd = 
# receiver email #
receiver_email = 

get_new_films()
send_film_of_the_week(bot_email, bot_passwd, receiver_email)
