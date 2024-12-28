
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

# 192.168.0.108

url = 'http://192.168.0.70:3000/garden_data'
json_str = '{ "sample_date": "2024-12-22 21:11:43", "actuator_east": "Closed", "actuator_west": "Closed", "moisture": "0", "temp_air_east": "47.08", "temp_soil_east": "55.62", "temp_air_west": "47.86", "temp_soil_west": "56.52", "temp_outside": "48.31", "temp_rpi": "91.76" }'
data = json_str.encode('utf-8');
headers = { "Content-Type": "application/json" }
# method is POST by default if data is provided

request = Request(url, data, headers)

try:
   with urlopen(request, timeout=10) as response:
       print('Response status: ' + str(response.status))
       print('Response body: \n' + str(response.read().decode("utf-8")))
except HTTPError as error:
    print('Response error.status: ' + str(error.status))
    print('Response error.reason: ' + str(error.reason))
except URLError as error:
    print(error.reason)
except TimeoutError:
    print("Request timed out")
