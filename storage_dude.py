import csv
import random as r

def filter_films(main_csv_file, temp_csv_file):
	with open(main_csv_file,'r+') as main_read:
   		existingFilms = [line for line in csv.reader(main_read, delimiter=',')]

	new = []
	with open(temp_csv_file,'r+') as temp_file:
   		temp_reader = csv.reader(temp_file, delimiter=',')
   		for row in temp_reader:
   			if row not in new and row not in existingFilms:
   				new.append(row)

	with open(main_csv_file, 'a') as f:
		csv_writer = csv.writer(f)
		for item in new:
			csv_writer.writerow(item)
	print('Films Filtered')

def pick_a_film(film_csv_file):
	with open(film_csv_file, 'r', encoding = 'utf-8') as f:
		csv_reader = csv.reader(f)
		data = list(csv_reader)
		picked_film = data[r.choice(range(1, len(data)))]
	return picked_film

def deliver_film_package(film_container):
	title = film_container[1]
	director = film_container[2]
	genre = film_container[3]
	year = film_container[4]
	country = film_container[5]
	sypnosis = film_container[6]
	mubi_take = film_container[7]
	image = film_container[8]
	
	package = [image, title, director, country, year, sypnosis, mubi_take, genre]
	return package

def execute_film_picking(file):
	p1 = pick_a_film(file)
	p2 = deliver_film_package(p1)
	return p2