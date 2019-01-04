"""
Weatherapp my project.
"""

import html
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864"
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