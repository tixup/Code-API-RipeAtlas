"""
PROMPT:

Write a Python script to query the RIPE Atlas API for the last 5 completed ping measurements from the past 2 months.
Use the endpoint https://atlas.ripe.net/api/v2/measurements/ with a GET request, 
including parameters: type='ping', status=2, page_size=5, and Unix timestamps for start/end time (using 'start_time__gte' and 'end_time__lte').
Set the header 'Authorization: Key <token>'.
Parse the JSON response, extracting measurements from the 'results' field.
Print each measurement's ID, 'target_ip', 'description', and 'start_time' (in UTC ISO format).
Use the datetime and dateutil.relativedelta modules.

"""


import requests
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Set the endpoint URL
url = "https://atlas.ripe.net/api/v2/measurements/"

# Set the authorization token
token = "066fa78b-d292-463a-bc86-57a84c0d9399"

# Set the request parameters
params = {
    "type": "ping",
    "status": 2,
    "page_size": 5,
    "start_time__gte": (datetime.now() - relativedelta(months=2)).timestamp(),
    "end_time__lte": datetime.now().timestamp()
}

# Make the GET request to the API
response = requests.get(url, headers={"Authorization": f"Key {token}"}, params=params)

# Parse the JSON response
data = json.loads(response.text)

# Extract the measurements from the 'results' field
measurements = data["results"]

# Print each measurement's ID, target_ip, description, and start_time (in UTC ISO format)
for measurement in measurements:
    print("ID:", measurement["id"])
    print("Target IP:", measurement["target_ip"])
    print("Description:", measurement["description"])
    print("Start Time:", datetime.fromtimestamp(measurement["start_time"]).isoformat())
    print()


"""
OUTPUT:

ID: 86731256
Target IP: 207.211.162.92
Description: Ping measurement to ordvmb.shanesvcn.net
Start Time: 2025-02-07T03:18:40

ID: 86741434
Target IP: 183.177.253.175
Description: Ping measurement to 183.177.253.175
Start Time: 2025-02-07T13:44:00

ID: 86743718
Target IP: 194.146.214.12
Description: Anchoring Mesh Measurement: Ping IPv4 for anchor ch-zrh-as25164.anchors.atlas.ripe.net
Start Time: 2025-02-07T15:33:47

...

"""