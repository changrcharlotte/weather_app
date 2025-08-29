from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import messagebox

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['gfg']['api']

def getweather(latlon):
    lat = latlon[0]
    lon = latlon[1]

    # keep your structure, just make placeholders match format() names
    url = 'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api_key}&units=metric'

    # define api_key somewhere accessible (global or passed in)
    # and choose which parts to exclude
    part = 'minutely,hourly,daily,alerts'
    result = requests.get(url.format(lat=lat, lon=lon, part=part, api_key=api_key))

    items = result.json()

    if items:
        temp = items['current']['temp']
        weather = items['current']['weather'][0]['main']
        return temp, weather
    else:
        raise SystemExit("No results")


def search():
    city = city_text.get()
    latlon = get_geocode(city)
    weather = getweather(latlon)

    if weather:
        location_lbl['text'] = city
        temperature_label['text'] = weather[0]
        weather_1['text'] = weather[1]
    else:
        messagebox.showerror('Error', "Cannot find {}".format(city))


def get_geocode(city):
    geo_url = "https://api.openweathermap.org/geo/1.0/direct"
    geo_params = {"q": city, "limit": 1, "appid": api_key}

    r = requests.get(geo_url, params=geo_params, timeout=10)
    if r.status_code != 200:
        raise SystemExit("Geocoding failed")

    places = r.json()  # <-- list
    if not places:
        raise SystemExit(f"No results for city: {city}")

    lat = places[0]["lat"]
    lon = places[0]["lon"]

    return lat, lon



app = Tk()

app.title("Weather App")
app.geometry("300x300")

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)#a type of tkinter component
city_entry.pack()

search_btn = Button(app, text="Search Weather", width=12, command=search)
search_btn.pack()
location_lbl = Label(app, text="Location", font={'bold',20})
location_lbl.pack()
temperature_label= Label(app, text ="")
temperature_label.pack()

weather_1 = Label(app, text="")
weather_1.pack()

app.mainloop()

#extract key from configuration file

