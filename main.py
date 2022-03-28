from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
import time
import getting_url

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/temperature', methods=['POST'])
def temperature():
    city_name =request.form['city']
    API_Key = '386df314be53675038e1916ba83dcee8'
    base_url = "https://api.openweathermap.org/data/2.5/weather?"+"appid=" + API_Key+ "&q="+ city_name
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    utc_time = datetime.utcnow()
    r = requests.get(base_url)
    json_object = r.json()
    try:
        temp = int(int(json_object['main']['temp'])-273.15)
        temp_feel = int(int(json_object['main']['feels_like'])-273.15)
        wind = int(json_object['wind']['speed']*3.6)
        pressure= json_object['main']['pressure']
        hum = json_object['main']['humidity']
        desc = json_object['weather'][0]['description']
        cloud = json_object['clouds']['all']
        country = json_object['sys']['country']
        sunrise = time.strftime("%H:%M", time.localtime(int(json_object['sys']['sunrise'])))
        sunset = time.strftime("%H:%M", time.localtime(int(json_object['sys']['sunset'])))
        timezone= json_object['timezone']
        local = utc_time + timedelta(seconds=timezone)
        local_time = local.strftime("%H:%M")
    except KeyError:
        return render_template('keyerror.html', city_name = city_name)
    return render_template('temperature.html', temp = temp, city_name = city_name, temp_feel=temp_feel, \
        wind=wind, pressure=pressure, dt_string=dt_string, hum=hum, desc=desc, cloud=cloud, country=country,\
            sunrise = sunrise, sunset=sunset, timezone=timezone, local=local, utc_time=utc_time, local_time=local_time)

@app.context_processor
def utility_processor():
    def get_icon_url(icon):
        return getting_url.get_url(icon)
    return {"get_icon_url": get_icon_url}


if __name__ == '__main__':
    app.run(debug=True)