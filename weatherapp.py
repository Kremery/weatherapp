"""
Weatherapp my project.
Simple script for weather sites scrapping
"""
import sys
import html
import argparse
import configparser
from pathlib import Path
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

ACCU_URL = "https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864"
ACCU_TAGS = ('<span class="large-temp">','<span class="cond">')

DEFAULT_NAME = 'Kaniv'
DEFAULT_URL = 'https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864'
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'
CONFIG_LOCATION = 'location'
CONFIG_FILE = 'weatherapp.ini'



RP5_URL = "http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B0%D0%BD%D0%B5%D0%B2%D1%96"
RP5_TAGS = ('<span class="t_0" style="display: block;">', '<span class="t_0" style="display: block;">')


SINOPTIK_URL = "https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B0%D0%BD%D1%96%D0%B2"
SINOPTIK_TAGS = ('<p class="today-temp">','<div class="description"> <!--noindex-->')


def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64;)'}

def get_page_source(url):
    """функція, де ми отримуємо url і повертаємо html-код із сторінки,
       a function where we get a url and return html-code from the page
    """

    request = Request(url, headers=get_request_headers())
    page_sourse = urlopen(request).read()
    return page_sourse.decode('utf-8')
	

def get_tag_content(page_content, tag):
    """тут знаходимо потрібний текст
        this function finds the right content
    """
    tag_index = page_content.find(tag)
    tag_size = len(tag)
    value_start = tag_index + tag_size

    content = ''
    for c in page_content[value_start:]:
        if c != '<':
            content += c
        else:
            break
    return content


def get_locations(locations_url):
    """
    """
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')
    
    locations = []
    for location in soup.find_all('li', {'class': 'drilldown cl'}):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url)) 
    return locations


def get_configuration_file():
    '''функція що повертає шлях для зберігання файлу. По замовчуванню це диреторія користувача
       a function that returns the path for file storage. By default, this is the user's directory
    '''
    return Path.home() / CONFIG_FILE

def save_configuration(name, url):
    """функція що зберігає вибрану локацію
       save the selected location
    """

    parser = configparser.Configparser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file(), 'w') as configfile:
        parser.write(configfile)
    

def get_
    '''функція що повертаю назву і адресу з файлу конфігурації
       the function that returns the name and address from the configuration file
    '''
    name = DEFAULT_NAME
    url = DEFAULT_URL
    parser = configparser.Configparser
    parser.read(get_configuration_file())

    config = parser[CONFIG_LOCATION]
    name, url = config['name'], config['url']
    return name, url

def configurate():
    """виводить список локацій
       displays a list of locations
    """

    locations = get_locations(ACCU_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations(location[1])
    
    save_configuration(*location) # save the selected location


def get_weather_info(page_content):
    """get information about the weather conditions from the site
       функція повертає інформацію про стан погоди 
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    
    current_day_section = city_page.find(
        'li', class_='day current first cl')#weather information per day

    if current_day_section == None:
        current_day_section = city_page.find(
        'li', class_='night current first cl')#weather information per night

    weather_info = {}#tuple with weather information

    current_day_url = current_day_section.find('a').attrs['href']
    if current_day_url:
        current_day_page = get_page_source(current_day_url)
        if current_day_page:
            current_day = \
                BeautifulSoup(current_day_page, 'html.parser')
            weather_details = \
                current_day.find('div', attrs={'id': 'detail-now'})
				
            condition = weather_details.find('span', class_='cond')#weather information
            if condition:
                weather_info['cond'] = condition.text
				
            temp = weather_details.find('span', class_='large-temp')#temperature information
            if temp:
                weather_info['temp'] = temp.text
				
            feal_temp = weather_details.find('span', class_='small-temp')#temperature feels information
            if feal_temp:
                weather_info['feal_temp'] = feal_temp.text
				
            '''wind_info = weather_details.find_all('li', class_='wind')
            if wind_info:
                weather_info['wind'] = \
                ' '.join(map(lambda t: t.text.strip(), wind_info))'''

            stats_info = weather_details.find_all('ul', class_='stats')#information fom the block stats
            if stats_info:
                weather_info['stats'] = \
                ' '.join(map(lambda t: t.text.strip(), stats_info))

    return weather_info


def produce_output(info):
    """функція що виводить в консоль інформацю із сайта Accuweather
       function that displays information from site Accuweather
    """

    print('Accu Weather: \n')
    print(f'{city_name}')
    print('+'*20)

    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def get_accu_weather_info():
    """функція, яка поверне інформацію про стан погоду за url-адресою, яку збережено у файлі концігурації
       a function that returns the weather state information at the url-address stored in the concatenation file
    """

    city_name, city_url = get_configuration()
    content = get_page_source(city_url)
    produce_output(city_name, get_weather_info(content))


def main(argv):
    """ Main entry point.
    """

    # KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5', 'sinoptik': 'SINOPTIK'}
    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      'config': configurate}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)

    '''weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS), 
                                    "RP5": (RP5_URL, RP5_TAGS), 
                                    "SINOPTIK": (SINOPTIK_URL, SINOPTIK_TAGS)} 
                                    '''
    #, "PR5": (RP5_URL, RP5_TAGS)}

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command]()
        else:
            print("Unknown command provided!")
            sys.exit(1)

    

if __name__ == '__main__':
    main(sys.argv[1:])


# v 1.24.40 