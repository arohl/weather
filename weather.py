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
(label, temp, unit) = sum_data["current_temp"]
degree = unit
print("%.1f%sC" % (temp, unit))
time_now = datetime.now().strftime('%-I:%M %p')
print("---")
print ("%s Observations @ %s | color=royalblue" %(location["name"], time_now))
print ("Current: %.1f%sC | color=black" % (temp, unit))
(label, feel_temp, unit) = sum_data["temp_feels_like"]
print ("Feels like: %.1f%sC | color=black" % (feel_temp, unit))
(label, value, unit) = sum_data["temp_now"]
if label == "Max":
  print ("Maximum: %d%sC | color=black" % (value, unit))
(label, value, unit) = sum_data["temp_later"]
if label == "Max":
  print ("Maximum: %d%sC | color=black" % (value, unit))
(label, value, unit) = sum_data["precis"]
print ("Conditions: %s | color=black" % (value[:-1]))
weather = api.WeatherApi(search=my_location, debug=0)
obs = weather.observations()
forecast = weather.forecasts_daily()
print("Humidity: %d%% | color=black" % (obs["humidity"]))
print("Wind: %s @ %d kmh | color=black" % (obs["wind"]["direction"], obs["wind"]["speed_kilometre"]))
sunrise = forecast[0]["astronomical"]["sunrise_time"]
sunset = forecast[0]["astronomical"]["sunset_time"]
print("Sunrise: %s | color=black" % (convert_date(sunrise).strftime("%-I" + ":" + "%M %p")))
print("Sunset: %s | color=black" % (convert_date(sunset).strftime("%-I" + ":" + "%M %p")))
if (obs["rain_since_9am"] > 0):
  print("Rain since 9 am: %d mm | color=black" %(obs["rain_since_9am"]))
print("---")
print (location["name"] + " Forecast | color=royalblue")
forecast.pop(0)
for f in forecast:
	if f["temp_min"] is None:
		temp_min = "--"
	else:
		temp_min = f["temp_min"]

	if f["temp_max"] is None:
		temp_max = "--"
	else:
		temp_max = f["temp_max"]
   
	date = convert_date(f["date"])
	formatted_date = date.strftime("%A")
	if f['short_text'] is not None:
	  print("%s Min: %d%sC, Max: %d%sC, %s | color=black" % (formatted_date, temp_min, degree, temp_max, degree, f["short_text"][:-1]))
	if f['extended_text'] is not None:
		print("--" + f["extended_text"][:-1] + " | size=12 color=black")
	
print("---")
print("Rain Radar | color=royalblue")
print(location["name"] + " | color=black href=http://www.bom.gov.au/products/IDR703.loop.shtml#skip")
print("National | color=black href=http://www.bom.gov.au/products/national_radar_sat.loop.shtml")
