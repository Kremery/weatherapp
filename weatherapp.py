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
from urllib.parse import quote
from bs4 import BeautifulSoup


ACCU_URL = "https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864"
ACCU_TAGS = ('<span class="large-temp">','<span class="cond">')

DEFAULT_NAME = 'Канів'
DEFAULT_URL = 'https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864'
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'
CONFIG_LOCATION = 'location_accu'
CONFIG_FILE = 'weatherapp.ini'
INFOWEATHER = 'infoweather'
INFOWEATHER_FILE = 'infoweather.txt'




RP5_URL = "http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B0%D0%BD%D0%B5%D0%B2%D1%96"
RP5_TAGS = ('<span class="t_0" style="display: block;">', '<span class="t_0" style="display: block;">')

DEFAULT_NAME_RP5 = 'Канів'
DEFAULT_URL_RP5 = 'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B0%D0%BD%D0%B5%D0%B2%D1%96'
RP5_BROWSE_LOCATIONS = 'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96'
CONFIG_FILE_RP5 = 'weatherapp_rp5.ini'
CONFIG_LOCATION_RP5 = 'locations_rp5'

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
    """Вибір локацій для Accuweather
       location selection from Accuweather
    """
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')
    
    locations = []
    for location in soup.find_all('li', {'class': 'drilldown cl'}):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url)) 
    return locations


def get_locations_rp5(locations_url):
    """Вибір локацій для RP5
       location selection from RP5
    """
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')
    
    # import pdb; pdb.set_trace()
    locations = []
    url_add = 'http://rp5.ua/'
    drilldown = soup.find_all('div', class_='country_map_links')
    if drilldown: 
        for location in drilldown:
            url = url_add + quote(location.find('a').attrs['href'])
            location = location.find('a').text
            locations.append((location, url))
    else: 
        drilldown = soup.find('div', class_='countryMap')
        if drilldown:
            for location in drilldown.find_all('h3'):
                url = url_add + quote(location.find('a').attrs['href'])
                location = location.find('a').text
                locations.append((location, url))

    return locations


def get_configuration_file():
    '''функція що повертає шлях для зберігання файлу.
       a function that returns the path for file storage. 
    '''
    return Path.cwd() / CONFIG_FILE

def save_configuration(name, url):
    """функція що зберігає вибрану локацію
       save the selected location
    """
    # import pdb; pdb.set_trace()
    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file(), 'w') as configfile:
        parser.write(configfile)


def get_configuration_file_rp5():
    '''функція що повертає шлях для зберігання файлу .
       a function that returns the path for file storage for site RP5.
    '''
    return Path.cwd() / CONFIG_FILE_RP5

def save_configuration_rp5(name, url):
    """функція що зберігає вибрану локацію
       save the selected location
    """
    # import pdb; pdb.set_trace()
    parser = configparser.ConfigParser(strict=False, interpolation=None)
    parser[CONFIG_LOCATION_RP5] = {'name': name, 'url': url}
    with open(get_configuration_file_rp5(), 'w') as configfile:
        parser.write(configfile)
    

def get_configuration():
    '''функція що повертає назву і адресу з файлу конфігурації
       the function that returns the name and address from the configuration file
    '''
    name = DEFAULT_NAME
    url = DEFAULT_URL
    parser = configparser.ConfigParser()
    parser.read(get_configuration_file())

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']
    
    return name, url


def get_configuration_rp5():
    '''функція що повертає назву і адресу з файлу конфігурації
       the function that returns the name and address from the configuration file
    '''
    name = DEFAULT_NAME_RP5
    url = DEFAULT_URL_RP5
    parser = configparser.ConfigParser()
    parser.read(get_configuration_file_rp5())

    if CONFIG_LOCATION_RP5 in parser.sections():
        config = parser[CONFIG_LOCATION_RP5]
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


def configurate_rp5():
    """виводить список локацій
       displays a list of locations
    """
    locations = get_locations_rp5(RP5_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations_rp5(location[1])
    
    save_configuration_rp5(*location) # save the selected location for rp5


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


def produce_output(city_name, info):
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
    

def get_infoweather_file():
    '''функція що повертає шлях для зберігання файлу про стан погоди. По замовчуванню це диреторія користувача
       a function that returns the way to save the file about the weather. By default, this is the user's directory
    '''
    return Path.home() / INFOWEATHER_FILE

def save_infoweather_to_file(city_name, info):
    """
    """
    with open(get_infoweather_file(), 'w') as infoweatherfile:
        infoweatherfile.write(f'\n AccuWeather')
        infoweatherfile.write(f'City: {city_name}\n')
        infoweatherfile.write('-' * 20)
        for key, value in info.items():
            infoweatherfile.write(f'\n{key}: {html.unescape(value)}')
        print('\nFile infoweather.txt has been saved to:')
        print(get_infoweather_file())


def save_infoweather():
    """ функція що зберігає інформацію про погоду у файл
       saves weather information to a file
    """

    city_name, city_url = get_configuration()
    content = get_page_source(city_url)
    save_infoweather_to_file(city_name, get_weather_info(content))


def main(argv):
    """ Main entry point.
    """

    # KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5', 'sinoptik': 'SINOPTIK'}
    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      # 'rp5': get_rp5_weather_info,
                      'config': configurate,
                      'config_rp5': configurate_rp5,
                      'iws': save_infoweather}

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