### This file (mubilifier.py) is the one responsible for dealing with the MUBI website, it does all the scraping and data cleaning needed ###
import requests
import re
from bs4 import BeautifulSoup
import json, csv

## data cleaning functions ##
# remove extra lines on strings and lists #
def clean_lines(txt):
    if type(txt) == str:
        p1 = re.sub('\n', '', txt)
        return p1
    elif type(txt) == list:
        arrP1 = []
        for item in txt:
            arrP1.append(re.sub('\n', '', item))
        return arrP1
# removes extra whitespace on strings #
def clean_whitespace(txt):
    p1 = re.sub(' +', '', txt)
    return p1

## functions for making the film id ##
# get name initials (ex: Ethan Cohen == EC) #
def get_name_initials(arr):
    if type(arr) == list:
        arrP1 = []
        for name in arr:
            p1 = name.split(' ')
            arrP1.append([x[0] for x in p1])
        arrP2 = []
        for initial in arrP1:
            arrP2.append(''.join(initial))
        return '/'.join(arrP2)
    elif type(arr) == str:
        arrP1 = []
        p1 = arr.split(' ')
        for name in p1:
            arrP1.append(name[0])
        return ''.join(arrP1)
# get countries first three letters (ex: Germany == Ger) #
def get_country_initials(arr):
    arrP1 = []
    for item in arr:
        arrP1.append(item[:3])
    arrP2 = []
    for con in arrP1:
        arrP2.append(''.join([con[i:i+1] for i in range(0, len(con), 1)]))
    return '.' + ''.join(arrP2) + '.'
# get film title initials (ex: The Lord of the Rings == TLOTR)
def get_title_initials(txt):
    txt = list(filter(None, txt.split(' ')))
    p1 = [a[0] for a in txt]
    return '-' + ''.join(p1)

## web scrapping functions ##
# extract all the films from the showing on the main page and outputs them in a list #
def find_all_films_links(source, output):
    for link in source:
        p1 = link.get('href')
        output.append('https://mubi.com/' + p1)
    print('Film links extracted')
# extracts film info and appends it with an id to an output list #
def get_film_info(inArr, output):
    for url in inArr:
        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content, 'lxml')
        # finding film title, year and genres #
        title = clean_lines(soup.find('span', attrs={'class': 'film-sticky__title'}).text)
        year = soup.find('span', attrs={'itemprop': 'dateCreated'}).text
        genres = clean_lines(soup.find('div', attrs={'class': 'film-show__genres'}).text.split(', '))
        # finding film directors and countries #
        film_country= clean_lines(soup.find('div', attrs={'class': 'film-show__country-year'}).text)[:-6].split(', ')
        director = clean_lines(soup.find('span', attrs={'class': 'film-sticky__title listed-directors'}).text)
        # searching for film sypnosis #
        sypnosis = soup.find('div', attrs={'class': 'film-show__descriptions__synopsis'}).find('p').text
        # finding MUBI take on the film #
        if soup.find('div', attrs={'class': 'film-show__descriptions__our-take'}) == None:
            mubi_take = 'No MUBI description of this Film'
        else:
            mubi_take = soup.find('div', attrs={'class': 'film-show__descriptions__our-take'}).find('p').text
        # searching for the film poster/image #
        poster = soup.find('meta', attrs={'class': 'js--film-still-url'})['content']
        # creating an ID for the film storing #
        film_id = get_name_initials(director) + get_title_initials(title) + get_country_initials(film_country) + year[2:]
        organizer = [film_id, title, director, genres, year, film_country, sypnosis, mubi_take, poster]
        output.append(organizer)
    print('Films Info Recollected')

## compiled function ##  
def execute_main(file):
    # goes to the main url and searches for all the displaying films #
    url = 'https://mubi.com/showing'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    source = soup.find_all('a', attrs={'class': 'full-width-tile__link'})
    # stores all the displaying films in a list #
    film_links = []
    find_all_films_links(source, film_links)
    # gets every film info #
    temp_film_info = []
    get_film_info(film_links, temp_film_info)
    with open(file, 'w', newline='') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(['Id', 'Title', 'Director', 'Genres', 'Year', 'Country', 'Sypnosis', 'MUBI Take', 'Poster'])
        for single_film in temp_film_info:
            writer.writerow(single_film)
    print('File Created')