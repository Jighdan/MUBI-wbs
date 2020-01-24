import requests
import re
from bs4 import BeautifulSoup
import json, csv

def clean_lines(txt):
    p1 = re.sub('\n', '', txt)
    return p1

def clean_whitespace(txt):
    p1 = re.sub(' +', '', txt)
    return p1

def get_name_initials(arr):
    arrP1 = []
    for name in arr:
        p1 = name.split(' ')
        arrP1.append([x[0] for x in p1])
    arrP2 = []
    for initial in arrP1:
        arrP2.append(''.join(initial))
    return '/'.join(arrP2)

def get_country_initials(arr):
    arrP1 = []
    for item in arr:
        arrP1.append(item[:3])
    arrP2 = []
    for con in arrP1:
        arrP2.append(''.join([con[i:i+1] for i in range(0, len(con), 1)]))
    return '.' + ''.join(arrP2) + '.'

def get_title_initials(txt):
    # split by title by whitespace #
    # take and return all the initials as a string #
    p1 = txt.split(' ')
    p2 = [a[0] for a in p1]
    return '-' + ''.join(p2)

def find_all_films_links(source, output):
    for link in source:
        p1 = link.find('div', attrs={'class': 'full-width-tile__read-more riforma-header'})
        output.append('https://mubi.com' + p1.find('a').get('href'))
    print('Film links Added')

def get_film_info(inArr, output):
    for url in inArr:
        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content, 'lxml')
        # finding film title and year #
        title = clean_lines(soup.find('h1', attrs={'class': 'film-show__titles__title riforma-header'}).text)
        year = soup.find('span', attrs={'itemprop': 'dateCreated'}).text
        # finding film directors and countries #
        film_country= clean_lines(soup.find('div', attrs={'class': 'film-show__country-year'}).text)[:-6].split(', ')
        director = clean_lines(soup.find('span', attrs={'class': 'film-sticky__title listed-directors'}).text).split(', ')
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
        organizer = [film_id, title, director, year, film_country, sypnosis, mubi_take, poster]
        output.append(organizer)
    print('Films Info Recollected')
        
def execute_main(file):
    # goes to the main url and searches for all the displaying films #
    url = 'https://mubi.com/showing'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    source = soup.find_all('article', attrs={'class': 'full-width-tile full-width-tile--now-showing'})
    # stores all the displaying films in a list #
    film_links = []
    find_all_films_links(source, film_links)
    # gets every film info #
    temp_film_info = []
    get_film_info(film_links, temp_film_info)
    with open(file, 'w', newline='') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(['Id', 'Title', 'Director', 'Year', 'Country', 'Sypnosis', 'MUBI Take', 'Poster'])
        for single_film in temp_film_info:
            writer.writerow(single_film)
    print('File Created')