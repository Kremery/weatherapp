"""
Weather app my project.
"""


from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/kaniv/321864/weather-forecast/321864"
#N1
#response = urlopen(ACCU_URL)

#N2
headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64;)'}
accu_request = Request(ACCU_URL, headers=headers)
response = urlopen(accu_request)

print(response)