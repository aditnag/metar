# metar
Project Set Up:

1. Install the packages in requirements.txt
2. Python Version: 3.11
3. Use Postman for Testing the endpoint
4. wsgi.py is the main file

Running the app: flask run

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