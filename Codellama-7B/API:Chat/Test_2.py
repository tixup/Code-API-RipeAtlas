"""
PROMPT:

Based on the previously provided documentation, write a Python script to fetch the last 5 completed ping measurements 
from RIPE Atlas in the past year using German probes (country code 'DE'). Then fetch their results and calculate the average RTT (latency) per measurement. 
Ensure the model queries the 'avg' field from the individual results of each measurement, as 'rtt' may not be directly available."

"""

import requests
from datetime import datetime

# Set API key and base URL for RIPE Atlas API
api_key = "066fa78b-d292-463a-bc86-57a84c0d9399"
base_url = "https://atlas.ripe.net/api/v2/"

# Define parameters for querying completed ping measurements in the past year from German probes
params = {
    "type": "ping",
    "target": "8.8.8.8",
    "start_time__gte": datetime(2021, 1, 1).timestamp(),
    "stop_time__lte": datetime(2021, 12, 31).timestamp(),
    "probe_ids": [
        {
            "country_code": "DE",
            "status_name": "Connected"
        }
    ],
    "af": 4
}

# Make GET request to retrieve completed ping measurements
response = requests.get(base_url + "measurements/", headers={"Authorization": f"Key {api_key}"}, params=params)
data = response.json()

# Extract measurement IDs and associated probe IDs for each completed measurement
measurement_ids = [result["id"] for result in data["results"]]
probe_ids = [result["prb_id"] for result in data["results"]]

# Initialize list to store average RTT values per measurement
avg_rtts = []

# Loop through each completed ping measurement and fetch its results
for measurement_id, probe_id in zip(measurement_ids, probe_ids):
    # Define parameters for querying results of a single measurement
    params = {
        "type": "ping",
        "target": "8.8.8.8",
        "start_time__gte": datetime(2021, 1, 1).timestamp(),
        "stop_time__lte": datetime(2021, 12, 31).timestamp(),
        "probe_ids": [
            {
                "id": probe_id
            }
        ],
        "af": 4
    }
    
    # Make GET request to retrieve results of a single measurement
    response = requests.get(base_url + f"measurements/{measurement_id}/", headers={"Authorization": f"Key {api_key}"}, params=params)
    data = response.json()
    
    # Extract average RTT value from results
    avg_rtts.append(data["avg"])
    
# Calculate and print the average RTT per measurement
print("Average RTT per measurement:")
for i, rtt in enumerate(avg_rtts):
    print(f"Measurement {i+1}: {rtt} ms")


"""
OUTPUT: 

File "/Users/matteotognetti/Desktop/uni/TESI/Codellama-7B/API:Chat/Test_2.py", line 29, in <module>
    probe_ids = [result["prb_id"] for result in data["results"]]
File "/Users/matteotognetti/Desktop/uni/TESI/Codellama-7B/API:Chat/Test_2.py", line 29, in <listcomp>
    probe_ids = [result["prb_id"] for result in data["results"]]
KeyError: 'prb_id'

Il codice prova a leggere result['prb_id'] da /measurements/, ma quel campo non è presente nella risposta di quel endpoint. 
È un campo che si trova nei risultati (/results/), non nei metadata della misurazione.

"""