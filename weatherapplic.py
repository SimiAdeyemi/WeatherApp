from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
import os

key = os.environ.get('API_key')

url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config["api_key"]["key"]


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (city, country, temp_celsius, temp_fahrenheit, icon, weather, description)
        city = json["name"]
        country = json["sys"]["country"]
        temp_kelvin = json["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (9/5)*(temp_kelvin - 273.15) + 32
        icon = json["weather"][0]["icon"]
        weather = json["weather"][0]["main"]
        description = json["weather"][0]["description"]
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather, description)
        return final

    else:
        return None


def search():

    global img
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl["text"] = '{}, {}'.format(weather[0], weather[1])
        img["file"] = "weather_icons/{}@2x.png".format(weather[4])
        temp_lbl["text"] = "{:.1f}°C, {:.1f}°F".format(weather[2], weather[3])
        weatherText_lbl["text"] = weather[5]
        description_lbl["text"] = weather[6]
    else:
        messagebox.showerror("Error", "Cannot find city {} ".format(city))


app = Tk()
app.title("Weather App")
app.geometry("600x375")
app["background"] = "#efd594"


city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text="Search Weather", width=12, command=search)
search_btn.pack()

location_lbl = Label(app, text="", font=("Helvetica", 20, "bold"), bg="#efd594", border=0)
location_lbl.pack()

img = PhotoImage(file="")
image = Label(app, image=img, bg="#efd594", border=0)
image.pack()

temp_lbl = Label(app, text="", font=("Helvetica", 18, "bold"), bg="#efd594", border=0)
temp_lbl.pack()

weatherText_lbl = Label(app, text="", font=("Helvetica", 12, "bold"), bg="#efd594", border=0)
weatherText_lbl.pack()

description_lbl = Label(app, text="", font=("Helvetica", 12, "bold"), bg="#efd594", border=0)
description_lbl.pack()

app.mainloop()
