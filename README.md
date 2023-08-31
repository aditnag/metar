# metar
Project Set Up:

1. Install the packages in requirements.txt: 
pip install -r requirements.txt 

2. Python Version: 3.11
3. Use Postman for Testing the endpoint
4. wsgi.py is the main file

**Running the app**: Open the project in you fav ide. 
Run the below command in the metar directory in the terminal:
=========
flask run
=========
eg: 
get request = http://localhost:8080/metar/info?scode=CYXQ.TXT&nocache=1

response:
{
    "data": {
        "station": "CYXQ",
        "last_observation": "2023/08/30 at 22:00 GMT",
        "temperature": "Not Updated C",
        "wind": "090 at 04 knots"
    }
}

If the value is not present in https://tgftp.nws.noaa.gov/data/observations/metar/stations/DNKN.TXT
the response will be **Not Updated**

eg: 
{
    "data": {
        "station": "DNKN",
        "last_observation": "2023/08/31 at 14:00 GMT",
        "temperature": "Not Updated C",
        "wind": "240 at 07 knots"
    }
}