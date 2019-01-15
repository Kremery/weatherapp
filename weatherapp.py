"""
Weatherapp my project.
"""

import html
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


def produce_output(provider_name, temp, condition):
	"""функція що виводить інформацю із сайтів
	   function that displays information from sites
	"""

	print(f'\n {provider_name}')
	print(f'Temperature: {html.unescape(temp)}\n')
	print(f'Condition: {html.unescape(condition)}\n')
	

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


def get_weather_info(page_content, tags):
	"""
	"""
	return tuple([get_tag_content(page_content, tag) for tag in tags])


def main():
	""" Main entry point.
	"""
	weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS), 
	                                "RP5": (RP5_URL, RP5_TAGS), 
	                                "SINOPTIK": (SINOPTIK_URL, SINOPTIK_TAGS)} 
	#, "PR5": (RP5_URL, RP5_TAGS)}
	for name in weather_sites:
		url, tags = weather_sites[name]
		content = get_page_source(url)
		temp, condition = get_weather_info(content, tags)
		produce_output(name, temp, condition)


if __name__ == '__main__':
	main()




'''
#N1
#response = urlopen(ACCU_URL)
#N2
# getting page from server
headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64;)'}
accu_request = Request(ACCU_URL, headers=headers)
accu_page = urlopen(accu_request).read()
#accu_page = str(accu_page)
accu_page = accu_page.decode('utf-8')
#here is the temperature
ACCU_TEPM_TAG = '<span class="large-temp">'
accu_temp_tag_size = len(ACCU_TEPM_TAG)
accu_tepm_tag_index = accu_page.find(ACCU_TEPM_TAG)
accu_temp_value_start = accu_tepm_tag_index + accu_temp_tag_size
accu_temp = ''
for char in accu_page[accu_temp_value_start:]:
	if char != '<':
		accu_temp += char
	else:
		break
#тут виводимо дані стану погоди
#here is the weather
ACCU_COND_TAG = '<span class="cond">'
accu_cond_tag_size = len(ACCU_COND_TAG)
accu_cond_tag_index = accu_page.find(ACCU_COND_TAG)
accu_cond_value_start = accu_cond_tag_index + accu_cond_tag_size
accu_cond = ''
for char in accu_page[accu_cond_value_start:]:
	if char != '<':
		accu_cond += char
	else:
		break
		
print('AccuWeather in Kaniv: \n')
print(f'Temperature: {html.unescape(accu_temp)}\n')
print(f'Weather: {accu_cond}\n')
#print("PAGE: ", accu_page) 
#this site rp5.ua
RP5_URL = "http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B0%D0%BD%D0%B5%D0%B2%D1%96"
#headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64;)'}
rp5_request = Request(RP5_URL, headers=headers)
rp5_page = urlopen(rp5_request).read()
rp5_content = rp5_page.decode('utf-8')
#here is the temperature
WINFO_CONTAINER_TAG = '<div id="ArchTemp">'
RP5_TEMP_TAG = '<span class="t_0" style="display: block;">'
rp5_temp_tag = rp5_content.find(RP5_TEMP_TAG, rp5_content.find(WINFO_CONTAINER_TAG))
rp5_temp_tag_size = len(RP5_TEMP_TAG)
#rp5_tepm_tag_index = rp5_content.find(rp5_temp_tag)
rp5_temp_tag_start = rp5_temp_tag + rp5_temp_tag_size
rp5_temp = ''
for char in rp5_content[rp5_temp_tag_start:]:
	if char != '<':
		rp5_temp += char
	else:
		break
#тут виводимо дані стану погоди
#here is the weather
AINFO_CONTAINER_TAG = '<div class="ArchiveInfo">'
RP5_ARCHIVE_TAG = '°F</span>'
rp5_archive_tag = rp5_content.find(RP5_ARCHIVE_TAG, rp5_content.find(AINFO_CONTAINER_TAG))
rp5_archive_tag_size = len(RP5_ARCHIVE_TAG)
#rp5_tepm_tag_index = rp5_content.find(rp5_temp_tag)
rp5_archive_tag_start = rp5_archive_tag + rp5_archive_tag_size + 2
rp5_archive = ''
for char in rp5_content[rp5_archive_tag_start:]:
	if char != '<':
		rp5_archive += char
	else:
		rp5_archive = rp5_archive + '.'
		break
		
print('RP5 in Kaniv: \n')
print(f'Temperature: {html.unescape(rp5_temp)}\n')
print(f'Weather: {rp5_archive}\n')
#this site sinoptik.ua
SINOPTIK_URL = "https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B0%D0%BD%D1%96%D0%B2/10-%D0%B4%D0%BD%D1%96%D0%B2"
#headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64;)'}
sinoptik_request = Request(SINOPTIK_URL, headers=headers)
sinoptik_page = urlopen(sinoptik_request).read()
sinoptik_content = sinoptik_page.decode('utf-8')
#here is the temperature
SINFO_CONTAINER_TAG = '<div class="lSide">'
SINOPTIK_TEMP_TAG = '<p class="today-temp">'
sinoptik_temp_tag = sinoptik_content.find(SINOPTIK_TEMP_TAG, sinoptik_content.find(SINFO_CONTAINER_TAG))
sinoptik_temp_tag_size = len(SINOPTIK_TEMP_TAG)
#rp5_tepm_tag_index = rp5_content.find(rp5_temp_tag)
sinoptik_temp_tag_start = sinoptik_temp_tag + sinoptik_temp_tag_size
sinoptik_temp = ''
for char in sinoptik_content[sinoptik_temp_tag_start:]:
	if char != '<':
		sinoptik_temp += char
	else:
		break
#тут виводимо дані стану погоди
#here is the weather
SSINFO_CONTAINER_TAG = '<div class="wDescription clearfix">'
SINOPTIK_ARCHIVE_TAG = '<div class="description"> <!--noindex-->'
sinoptik_archive_tag = sinoptik_content.find(SINOPTIK_ARCHIVE_TAG, sinoptik_content.find(SSINFO_CONTAINER_TAG))
sinoptik_archive_tag_size = len(SINOPTIK_ARCHIVE_TAG)
#rp5_tepm_tag_index = rp5_content.find(rp5_temp_tag)
sinoptik_archive_tag_start = sinoptik_archive_tag + sinoptik_archive_tag_size
sinoptik_archive = ''
for char in sinoptik_content[sinoptik_archive_tag_start:]:
	if char != '<':
		sinoptik_archive += char
	else:
		break
		
print('SINOPTIK.UA in Kaniv: \n')
print(f'Temperature: {html.unescape(sinoptik_temp)}\n')
print(f'Weather: {sinoptik_archive}\n')
'''