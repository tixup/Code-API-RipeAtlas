"""
PROMPT:

Write a Python script that queries the RIPE Atlas REST API to retrieve the last 5 ping-type measurements completed in the last 60 days.

For each measure, the script must:
1. Set up a GET request to the RIPE Atlas API endpoint:
   https://atlas.ripe.net/api/v2/measurements/ and retrieve the measurements with parameters such as type, status ('2'), page_size ('5') and start/end time. 
   Need to convert dates to integer timestamps.
2. Print the measure ID, target IP (target_ip), description (description), and start time in UTC ISO format. Use the `datetime` module and `relativedelta` from `dateutil`.

The RIPE Atlas API requires an API key header for authentication. Use `Authorization: Key <token>` in your headers.

"""

import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Set up the API endpoint and headers
endpoint = "https://atlas.ripe.net/api/v2/measurements/"
headers = {"Authorization": f"Key 066fa78b-d292-463a-bc86-57a84c0d9399"}

# Set up the parameters for the GET request
params = {
    "type": "ping",
    "status": "2",
    "page_size": "5",
    "start_time": (datetime.utcnow() - relativedelta(days=60)).isoformat(),
    "end_time": datetime.utcnow().isoformat()
}

# Make the GET request and parse the response as JSON
response = requests.get(endpoint, headers=headers, params=params)
data = response.json()

# Print the results
for measurement in data["measurements"]:
    print("Measurement ID:", measurement["id"])
    print("Target IP:", measurement["target_ip"])
    print("Description:", measurement["description"])
    print("Start time (UTC ISO format):", measurement["start_time"])
    print("\n")


"""
OUTPUT:

File "/Users/matteotognetti/Desktop/uni/TESI/Codellama-7B/Test_1.py", line 38, in <module>
    for measurement in data["measurements"]:
KeyError: 'measurements'

(il token giusto era "results", da Documentazione RIPE Atlas)
(sbagliato comunque il formato di start e end time, non sono 'int')
(non usando start_time__gte, è difficle ottenere risultati che iniziano proprio in quello start_time)

"""