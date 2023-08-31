import re, time
import requests
from flask import request, jsonify
import redis
import json
from application.v1.resources.Resources import (
    API_Resource,
    NameSpace,
)
api = NameSpace("Metar weather service")
indents = 4

cache = redis.Redis(host='localhost', port=6379, db=0)
CACHE_EXPIRATION = 300  # 5 minutes


# function to fetch weather data from the METAR URL
def fetch_metar_data(station_code):
    try:
        url = f'http://tgftp.nws.noaa.gov/data/observations/metar/stations/{station_code}'
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if HTTP request fails
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching METAR data: {str(e)}"


# function to parse METAR data and extract relevant information
def parse_metar_data(data):
    try:
        lines = data.strip().split()
        station = lines[2]

        observation_date = lines[0]
        time = lines[1]

        direction = ""
        velocity = ""
        gust = ""
        for i in range(2, len(lines)):
            if lines[i][-2:] == "KT":
                wind_direction = lines[i]
                if len(lines[i]) == 7:
                    direction = lines[i][:3]
                    velocity = lines[i][3:-2]
                    break
                elif len(lines[i]) == 10:
                    direction = lines[i][:3]
                    velocity = lines[i][-4:-2]
                    gust = lines[i][3:6]
                    break

        # M01 / M05
        temperature = ""
        dew = ""
        for item in lines:
            if item[0] == "M" and item[4] == "M":
                temperature = "-".join(item[1:3])
                dew = "-"+item[-2:]
            elif item[0] == "P" and item[4] == "P":
                temperature = "-".join(+item[1:3])
                dew = item[-2:]
            else:
                temperature = "Not Updated"
                dew = "Not Update"

        return {
            "station": station,
            "last_observation": f"{observation_date} at {time} GMT",
            "temperature": temperature,
            "wind_direction": direction,
            "wind_speed": velocity
        }
    except Exception as e:
        return f"Error parsing METAR data: {str(e)}"


class WeatherInfo(API_Resource):
    """Get Wheather Details """

    @api.doc(params={'scode': 'Station code', 'nocache': '0 to use cache, 1 to fetch data'})
    # @api.route('/metar/info')
    def get(self):
        try:
            start = time.time()
            station_code = request.args.get('scode')
            nocache = request.args.get('nocache')

            if nocache == '1':
                data = fetch_metar_data(station_code)
                cache.set(station_code, data, ex=CACHE_EXPIRATION)
            else:
                cached_data = cache.get(station_code)
                if cached_data:
                    data = cached_data.decode('utf-8')
                else:
                    data = fetch_metar_data(station_code)
                    cache.set(station_code, data, ex=CACHE_EXPIRATION)

            parsed_data = parse_metar_data(data)
            response = {
                "station": station_code,
                "last_observation": parsed_data["last_observation"],
                "temperature": parsed_data["temperature"] + " C",
                "wind": f"{parsed_data['wind_direction']} at {parsed_data['wind_speed']} knots",
            }
            end = time.time()
            print(f"time taken = {end - start}")
            # return json.dumps({"data": response})
            return json.loads(json.dumps({"data": response}))
        except Exception as e:
            return json.dumps({"error": str(e)})
