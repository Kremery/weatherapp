"""
Weatherapp my project.
"""
import sys
import html
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864"
ACCU_TAGS = ('<span class="large-temp">','<span class="cond">')

RP5_URL = "http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B0%D0%BD%D0%B5%D0%B2%D1%96"
#RP5_TAGS = (rp5_content.find(RP5_TEMP_TAG, rp5_content.find(WINFO_CONTAINER_TAG)), ',"°F</span>')
#WINFO_CONTAINER_TAG = '<div id="ArchTemp">'
#RP5_TEMP_TAG = '<span class="t_0" style="display: block;">'
RP5_TAGS = ('<span class="t_0" style="display: block;">', '<span class="t_0" style="display: block;">')


SINOPTIK_URL = "https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B0%D0%BD%D1%96%D0%B2"
SINOPTIK_TAGS = ('<p class="today-temp">','<div class="description"> <!--noindex-->')




def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64;)'}

def get_page_source(url):
    """функція, де ми отримуємо url,
       function where we get url
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


def get_weather_info(page_content):
	"""
	"""
    city_page = BeautifulSoup(page_content, 'html.parser')
	
    current_day_section = city_page.find(
        'li', class_='day current first cl')#weather information per day

    weather_info = {}#tuple with weather information

    if current_day_section:
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

    else:
        current_day_section = city_page.find(
        'li', class_='night current first cl')#weather information per night

			if current_day_section:
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
	"""функція що виводить інформацю із сайтів
	   function that displays information from sites
	"""

	print('Accu Weather: \n')

	for key, value in info.items():
		print(f'{key}: {html.unescape(value)}')

	"""print(f'\n {provider_name}')
	print(f'Temperature: {html.unescape(temp)}\n')
	print(f'Condition: {html.unescape(condition)}\n')
	"""

def main(argv):
	""" Main entry point.
	"""

	KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5', 'sinoptik': 'SINOPTIK'}

	parser = argparse.ArgumentParser()
	parser.add_argument('command', help='Service name', nargs=1)
	params = parser.parse_args(argv)

	weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS), 
	                                "RP5": (RP5_URL, RP5_TAGS), 
	                                "SINOPTIK": (SINOPTIK_URL, SINOPTIK_TAGS)} 
	#, "PR5": (RP5_URL, RP5_TAGS)}

	if params.command:
		command = params.command[0]
		if command in KNOWN_COMMANDS:
			weather_sites = {
				KNOWN_COMMANDS[command]: weather_sites[KNOWN_COMMANDS[command]]
			}
		else:
			print("Unknown command provided!")
			sys.exit(1)

	for name in weather_sites:
		url, tags = weather_sites[name]
		content = get_page_source(url)
		produce_output(get_weather_info(content))


if __name__ == '__main__':
	main(sys.argv[1:])
