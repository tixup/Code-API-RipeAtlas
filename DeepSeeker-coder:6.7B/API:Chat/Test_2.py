"""
QUERY:

Based on the previously provided documentation, write a Python script to fetch the last 5 completed ping measurements 
from RIPE Atlas in the past year using German probes (country code 'DE'). Then fetch their results and calculate the average RTT (latency) per measurement. 
Ensure the model queries the 'avg' field from the individual results of each measurement, as 'rtt' may not be directly available."

"""

import requests
from datetime import datetime, timedelta

# Set up authentication headers for the API request
headers = {
    "Authorization": "Key 066fa78b-d292-463a-bc86-57a84c0d9399"
}

# Calculate one year ago from now in unix timestamp format
one_year_ago = int((datetime.now() - timedelta(days=365)).timestamp())

params = {
    "type": "ping",
    "status_name": "Finished",  # Get only finished measurements
    "af": 4,  # IPv4
    "start_time__gte": one_year_ago,  # One year ago from now
}

# Send the initial request to get measurement ids
url = "https://atlas.ripe.net/api/v2/measurements/"
response = requests.get(url, headers=headers, params=params)
data = response.json()["results"]

# Filter out measurements not involving German probes
german_probes = ["DE1", "DE2",...]  # Replace with actual DE probe IDs - placeholder list
data = [x for x in data if str(x['prb_id']) in german_probes]

# Sort the data based on the measurement finish time
data.sort(key=lambda x: x["finished"], reverse=True)

top5_measurements = []
if len(data) > 5:
    top5_measurements = data[:5]
else:
    top5_measurements = data

for measurement in top5_measurements:
    # Send another request to get the results of this specific measurement
    url = f"https://atlas.ripe.net/api/v2/measurements/{measurement['pk']}/result/"
    response = requests.get(url, headers=headers)
    data = response.json()["results"]

    # Extract the 'rtt' values from each result entry and calculate average
    rtts = [float(x["rtt"]) for x in data]
    avg_rtt = sum(rtts)/len(rtts) if len(rtts) > 0 else 0
    
    print(f"Measurement ID: {measurement['pk']}, Average RTT: {avg_rtt}")


"""
OUTPUT:

raceback (most recent call last):
  File "/Users/matteotognetti/Desktop/uni/TESI/DeepSeek-coder/API:Chat/Test_quasi_3.py", line 35, in <module>
    data = [x for x in data if str(x['prb_id']) in german_probes]
  File "/Users/matteotognetti/Desktop/uni/TESI/DeepSeek-coder/API:Chat/Test_quasi_3.py", line 35, in <listcomp>
    data = [x for x in data if str(x['prb_id']) in german_probes]
KeyError: 'prb_id'

"""