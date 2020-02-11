from storage_dude import filter_films, execute_film_picking
from mubilifier import execute_main
from delivery_guy import content_generator, send_to_email
from datetime import date
import re

# user data #
with open('user_data.txt') as f:
    content = f.readlines()
    receiver_email = re.sub('\n', '', content[3])
    bot_email = re.sub('\n', '', content[6])
    bot_passwd = re.sub('\n', '', content[9])
	
# databases #
temp_data = 'record/temp_data.csv'
main_data = 'record/film_database.csv'

def get_new_films():
	# chose the days freely, MUBI.com/showing updates everyday #
	if date.today().strftime('%d') == '11' or date.today().strftime('%d') == '26':
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


get_new_films()
send_film_of_the_week(bot_email, bot_passwd, receiver_email)
