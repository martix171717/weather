from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/temperature', methods=['POST'])
def temperature():
    city_name = request.form['city']
    API_Key = '386df314be53675038e1916ba83dcee8'
    base_url = "https://api.openweathermap.org/data/2.5/weather?"+"appid=" + API_Key+ "&q="+ city_name
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    r = requests.get(base_url)
    json_object = r.json()
    try:
        temp = int(int(json_object['main']['temp'])-273.15)
        temp_feel = int(int(json_object['main']['feels_like'])-273.15)
        wind = int(json_object['wind']['speed']*3.6)
        pressure= json_object['main']['pressure']
    except KeyError:
        return render_template('keyerror.html', city_name = city_name)
    return render_template('temperature.html', temp = temp, city_name = city_name, temp_feel=temp_feel, \
        wind=wind, pressure=pressure, dt_string=dt_string)


if __name__ == '__main__':
    app.run(debug=True)