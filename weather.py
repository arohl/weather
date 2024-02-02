#!/usr/bin/env -P/Users/andrew/.asdf/shims/:/Users/180341c/.asdf/shims/:/opt/local/bin/:/Users/andrew/opt/anaconda3/bin:/Users/andrew/anaconda3/bin:/Users/180341c/opt/anaconda3/bin/    python3

# <bitbar.title>Kensington Weather</bitbar.title>
# <bitbar.version>v0.91</bitbar.version>
# <bitbar.author>Andrew Rohl</bitbar.author>
# <bitbar.author.github>arohl</bitbar.author.github>
# <bitbar.desc>Provides current temperature and 6 day forecast for Kensington</bitbar.desc>
# <bitbar.dependencies>python3, weather_au</bitbar.dependencies>

import sys
from weather_au import summary, api
from datetime import datetime
from dateutil.parser import parse

def convert_date(date):
  return (parse(date).astimezone())

my_location = '6151'
sum = summary.Summary(search=my_location)
location = sum.location
# check if the search produced a result (other methods will also return None if the search fails).
if location is None:
	print("!")
	print("---")
	print(f"Location not found: {my_location}")
	sys.exit()
sum_data = sum.summary()
(label, value, unit) = sum_data["precis"]
conditions = value[:-1]
if 'sunny'.casefold() in conditions.casefold():
    symbol = ":sun.max.fill:"
elif 'cloud'.casefold() in conditions.casefold():
    symbol = ":cloud.fill:"
elif 'clear'.casefold() in conditions.casefold():
    symbol = ":moon.fill:"
elif 'shower'.casefold() in conditions.casefold():
    symbol = ":cloud.rain.fill:"
elif 'rain'.casefold() in conditions.casefold():
    symbol = ":cloud.heavyrain.fill:"
elif 'storm'.casefold() in conditions.casefold():
	symbol = ":cloud.bolt.fill:"
elif 'smoke'.casefold() in conditions.casefold():
	symbol = ":smoke.fill:"

else:
    symbol = ":exclamationmark.triangle:"
(label, temp, unit) = sum_data['current_temp']
degree = unit
print(f"{symbol} {temp:.1f}{unit}C")
time_now = datetime.now().strftime('%-I:%M %p')
print("---")
print (f"{location['name']} Observations @ {time_now} | color=royalblue")
print (f"Current: {temp:.1f}{unit}C | color=black")
(label, feel_temp, unit) = sum_data["temp_feels_like"]
print (f"Feels like: {feel_temp:.1f}{unit}C | color=black")
(label, value, unit) = sum_data["temp_now"]
if label == 'Max':
	print (f"Maximum: {value}{unit}C | color=black")
(label, value, unit) = sum_data["temp_later"]
if label == 'Max':
	print (f"Maximum: {value}{unit}C | color=black")
(label, value, unit) = sum_data["precis"]
print (f"Conditions: {value[:-1]} | color=black")
weather = api.WeatherApi(search=my_location, debug=0)
obs = weather.observations()
forecast = weather.forecasts_daily()
print(f"Humidity: {obs['humidity']}% | color=black")
print(f"Wind: {obs['wind']['direction']} @ {obs['wind']['speed_kilometre']} kmh | color=black")
sunrise = forecast[0]['astronomical']['sunrise_time']
sunset = forecast[0]['astronomical']['sunset_time']
print(f"Sunrise: {convert_date(sunrise).strftime('%-I' + ':' + '%M %p')} | color=black")
print(f"Sunset: {convert_date(sunset).strftime('%-I' + ':' + '%M %p')} | color=black")
if (obs['rain_since_9am'] > 0):
	print(f"Rain since 9 am: {obs['rain_since_9am']} mm | color=black")
print("---")
print (location["name"] + " Forecast | color=royalblue")
forecast.pop(0)
for f in forecast:
	if f['temp_min'] is None:
		temp_min = "--"
	else:
		temp_min = f['temp_min']

	if f['temp_max'] is None:
		temp_max = "--"
	else:
		temp_max = f['temp_max']

	date = convert_date(f['date'])
	formatted_date = date.strftime('%a')
	if f['short_text'] is not None:
	  print(f"{formatted_date} :thermometer.snowflake: {temp_min}{degree}C, :thermometer.sun.fill: {temp_max}{degree}C, {f['short_text'][:-1]} | color=black")
	if f['extended_text'] is not None:
		print(f"--{f['extended_text'][:-1]} | size=12 color=black")

print("---")
print("Rain Radar | color=royalblue")
print(location["name"] + " | color=black href=http://www.bom.gov.au/products/IDR703.loop.shtml#skip")
print("National | color=black href=http://www.bom.gov.au/products/national_radar_sat.loop.shtml")
