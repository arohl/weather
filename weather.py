#!/Users/andrew/anaconda3/bin/python3
import sys
from weather_au import summary, api
from datetime import datetime
from dateutil.parser import parse

def convert_date(date):
    return (parse(date).astimezone())

my_location = "perth+wa"
sum = summary.Summary(search=my_location)
location = sum.location
# check if the search produced a result (other methods will also return None if the search fails).
if location is None:
	print("!")
	print("---")
	print("Location not found: " + my_location)
	sys.exit()
sum_data = sum.summary()
(label, value, unit) = sum_data["current_temp"]
degree = unit
print(str(value)+ unit + "C")
print("---")
print (location["name"] + " Observations | color=black")
print ("Current: " + str(value) + unit + "C" + " | color=dimgray")
(label, value, unit) = sum_data["temp_feels_like"]
print ("Feels like: " + str(value) + unit + "C" + " | color=dimgray")
(label, value, unit) = sum_data["temp_now"]
if label == "Max":
    print ("Maximum: " + str(value) + unit + "C" + " | color=dimgray")
(label, value, unit) = sum_data["precis"]
print ("Conditions: " + value[:-1] + " | color=dimgray")

weather = api.WeatherApi(search=my_location, debug=0)
obs = weather.observations()
forecast = weather.forecasts_daily()
print("Humidity: " + str(obs["humidity"]) + "% | color=dimgray")
print("Wind: " + obs["wind"]["direction"] + " @ " + str(obs["wind"]["speed_kilometre"]) + " kmh | color=dimgray" )
sunrise = forecast[0]["astronomical"]["sunrise_time"]
sunset = forecast[0]["astronomical"]["sunset_time"]
print("Sunrise: " + convert_date(sunrise).strftime("%-I" + ":" + "%-M %p") + " | color=dimgray")
print("Sunset: " + convert_date(sunset).strftime("%-I" + ":" + "%-M %p") + " | color=dimgray")
if (obs["rain_since_9am"] > 0):
	print("Rain since 9 am: " + str(obs["rain_since_9am"]) + " mm | color=dimgray")
print("---")
print (location["name"] + " Forecast | color=black")
forecast.pop(0)
for f in forecast:
    if f['temp_min'] is None:
        temp_min = '--'
    else:
        temp_min = f['temp_min']

    if f['temp_max'] is None:
        temp_max = '--'
    else:
        temp_max = f['temp_max']
    date = convert_date(f['date'])
    formatted_date = date.strftime("%A")
    print(formatted_date + " Min: " + str(temp_min) + degree + "C, Max: " + str(temp_max)  + degree + "C, " + f['short_text'][:-1] + " | color=dimgray")

