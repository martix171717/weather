from flask import Flask, render_template, request
import requests

def get_url(icon):
    base_url1 = "http://openweathermap.org/img/wn/"
    base_url2="@2x.png"
    city_name =request.form['city']
    API_Key = '386df314be53675038e1916ba83dcee8'
    base_url = "https://api.openweathermap.org/data/2.5/weather?"+"appid=" + API_Key+ "&q="+ city_name
    r = requests.get(base_url)
    json_object = r.json()
    icon = json_object['weather'][0]['icon']
    return f"{base_url1}{icon}{base_url2}"