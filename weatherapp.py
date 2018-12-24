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
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
accu_request = Request(ACCU_URL, headers=headers)
accu_page = urlopen(accu_request).read()
accu_page = str(accu_page)


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

#print(accu_temp_value_start)
#print(accu_temp)
print('AccuWeather: \n')
print(f'Temperature: {html.unescape(accu_temp)}\n')

#print(accu_page) 