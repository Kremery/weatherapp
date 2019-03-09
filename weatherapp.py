"""
Weatherapp my project.
Simple script for weather sites scrapping
"""
import sys
import html
import time
import hashlib
import argparse
import configparser
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote
from bs4 import BeautifulSoup

FAKE_MOZILLA_AGENT = 'Mozilla/5.0 (X11; Fedora; Linux x86_64;)'
CACHE_DIR = '.wappcache'
CACHE_TIME = 600


ACCU_URL = "https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864"
ACCU_TAGS = ('<span class="large-temp">','<span class="cond">')

DEFAULT_NAME = 'Канів'
DEFAULT_URL = 'https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864'
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'
CONFIG_LOCATION_ACCU = 'location_accu'
CONFIG_FILE_ACCU = 'weatherapp_accu.ini'
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
    """Returns custom headers for url requests.
    """

    return {'User-Agent': FAKE_MOZILLA_AGENT}


def get_cache_directory():
    '''функція що повертає шлях до директорії.
       Path to cache directory. 
    '''
    return Path.home() / CACHE_DIR


def get_url_hash(url):
    """Повертає унікальне ім'я файлу за url.
       Returns a unique file name for url.
    """

    return hashlib.md5(url.encode('utf-8')).hexdigest()


def save_cache(url, page_sourse):
    """Save page source data to file.
    """
    
    url_hash = get_url_hash(url)
    cache_dir = get_cache_directory()
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)
    
    with (cache_dir / url_hash).open('wb') as cache_file:
        cache_file.write(page_sourse)


def is_valid(path):
    """Check if current cache file is valid.
    """

    tttime = time.time() - path.stat().st_mtime

    return tttime < CACHE_TIME 


def get_cache(url):
    """Повертає дані кешу, якщо такі існюють.
       Return cache data if any.
    """
    
    cache = b''
    url_hash = get_url_hash(url)
    cache_dir = get_cache_directory()
    if cache_dir.exists():
        cache_path = cache_dir / url_hash
        if cache_path.exists() and is_valid(cache_path):
            with cache_path.open('rb') as cache_file:
                cache = cache_file.read()

    return cache


def get_page_source(url):
    """функція, де ми отримуємо url і повертаємо html-код із сторінки або з файлової системи (кешу),
       a function where we get a url and return html-code from the page or from a file system
    """

    cache = get_cache(url)
    if cache:
        page_sourse = cache
        print(f"Cache for {url}")
    else:
        request = Request(url, headers=get_request_headers())
        page_sourse = urlopen(request).read()
        save_cache(url, page_sourse)
    
    return page_sourse.decode('utf-8')
	

def get_locations_accu(locations_url):
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


def get_configuration_file_accu():
    '''функція що повертає шлях для зберігання файлу.
       a function that returns the path for file storage. 
    '''
    return Path.home() / CONFIG_FILE_ACCU

def save_configuration_accu(name, url):
    """функція що зберігає вибрану локацію
       save the selected location
    """
    
    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION_ACCU] = {'name': name, 'url': url}
    with open(get_configuration_file_accu(), 'w') as configfile:
        parser.write(configfile)


def get_configuration_file_rp5():
    '''функція що повертає шлях для зберігання файлу.
       a function that returns the path for file storage for site RP5.
    '''
    return Path.home() / CONFIG_FILE_RP5

def save_configuration_rp5(name, url):
    """функція що зберігає вибрану локацію
       save the selected location
    """
    
    parser = configparser.ConfigParser(strict=False, interpolation=None)
    parser[CONFIG_LOCATION_RP5] = {'name': name, 'url': url}
    with open(get_configuration_file_rp5(), 'w') as configfile:
        parser.write(configfile)
    

def get_configuration_accu():
    '''функція що повертає назву і адресу з файлу конфігурації для сайту AccuWeather
       the function that returns the name and address from the configuration file for site AccuWeather
    '''
    
    name = DEFAULT_NAME
    url = DEFAULT_URL
    parser = configparser.ConfigParser()
    parser.read(get_configuration_file_accu())

    if CONFIG_LOCATION_ACCU in parser.sections():
        config = parser[CONFIG_LOCATION_ACCU]
        name, url = config['name'], config['url']
    
    return name, url


def get_configuration_rp5():
    '''функція що повертає назву і адресу з файлу конфігурації
       the function that returns the name and address from the configuration file
    '''
    name = DEFAULT_NAME_RP5
    url = DEFAULT_URL_RP5
    parser = configparser.ConfigParser(strict=False, interpolation=None)
    parser.read(get_configuration_file_rp5())

    if CONFIG_LOCATION_RP5 in parser.sections():
        config = parser[CONFIG_LOCATION_RP5]
        name, url = config['name'], config['url']
    
    return name, url


def configurate_accu():
    """виводить список локацій
       displays a list of locations for site AccuWeather
    """
    locations = get_locations_accu(ACCU_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations_accu(location[1])
    
    save_configuration_accu(*location) # save the selected location


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


def get_weather_info_accu(page_content):
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
				
            condition = weather_details.find('span', class_='cond')#weather_cond information
            if condition:
                weather_info['cond'] = condition.text
				
            temp = weather_details.find('span', class_='large-temp')#temperature information
            if temp:
                weather_info['temp'] = temp.text
				
            feal_temp = weather_details.find('span', class_='small-temp')#temperature feels information
            if feal_temp:
                weather_info['feal_temp'] = feal_temp.text
				
            stats_info = weather_details.find_all('ul', class_='stats')#information fom the block stats
            if stats_info:
                weather_info['stats'] = \
                ' '.join(map(lambda t: t.text.strip(), stats_info))

    return weather_info


def get_weather_info_rp5(page_content):
    """get information about the weather conditions from the site RP5
       функція повертає інформацію про стан погоди з сайту RP5
    """
    city_page = BeautifulSoup(page_content, 'html.parser')
    
    current_day_section = city_page.find(
        'div', class_='ArchiveInfo')#weather information per day

    weather_info = {}#tuple with weather information
    if current_day_section:
        weather_info['weather_info'] = current_day_section.text
    
    return weather_info


def produce_output_accu(city_name, info):
    """функція що виводить в консоль інформацю із сайта Accuweather
       function that displays information from site Accuweather
    """
    
    print('Accu Weather: \n')
    print(f'{city_name}')
    print('+'*20)

    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def produce_output_rp5(city_name, info):
    """функція що виводить в консоль інформацю із сайта RP5
       function that displays information from site RP5
    """
    
    print('RP5: \n')
    print(f'{city_name}')
    print('=='*18)

    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def get_accu_weather_info():
    """функція, яка поверне інформацію про стан погоди для сайту Accuweather за url-адресою, яку збережено у файлі концігурації
       a function that returns the weather state information for site AccuWeather at the url-address stored in the concatenation file
    """

    city_name, city_url = get_configuration_accu()
    content = get_page_source(city_url)
    produce_output_accu(city_name, get_weather_info_accu(content))
    

def get_rp5_weather_info():
    """функція, яка поверне інформацію про стан погоди для сайту RP5 за url-адресою, яку збережено у файлі концігурації
       a function that returns the weather state information for site RP5 at the url-address stored in the concatenation file
    """
    
    city_name, city_url = get_configuration_rp5()
    content = get_page_source(city_url)
    produce_output_rp5(city_name, get_weather_info_rp5(content))


def get_infoweather_file():
    '''функція що повертає шлях для зберігання файлу про стан погоди. По замовчуванню це диреторія користувача
       a function that returns the way to save the file about the weather. By default, this is the user's directory
    '''
    return Path.home() / INFOWEATHER_FILE

def save_infoweather_to_file(city_name, info):
    """
    """
    import pdb; pdb.set_trace()
    with open(get_infoweather_file(), 'w') as infoweatherfile:
        infoweatherfile.write(f'\n AccuWeather')
        infoweatherfile.write(f'City: {city_name}\n')
        infoweatherfile.write('-' * 20)
        for key, value in info.items():
            # infoweatherfile.write(f'\n{key}: {value}')
            infoweatherfile.write(f'\n{key}: {html.unescape(value)}')
        print('\nFile infoweather.txt has been saved to:')
        print(get_infoweather_file())


def save_infoweather():
    """ функція що зберігає інформацію про погоду у файл
       saves weather information to a file
    """
    import pdb; pdb.set_trace()
    city_name, city_url = get_configuration_accu()
    content = get_page_source(city_url)
    save_infoweather_to_file(city_name, get_weather_info_accu(content))


def main(argv):
    """ Main entry point.
    """

    # KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5', 'sinoptik': 'SINOPTIK'}
    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      'rp5': get_rp5_weather_info,
                      'config_accu': configurate_accu,
                      'config_rp5': configurate_rp5,
                      'iws': save_infoweather}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command]()
        else:
            print("Unknown command provided!")
            sys.exit(1)

    

if __name__ == '__main__':
    main(sys.argv[1:])


# import pdb; pdb.set_trace()