"""
QUERY:

With the provided documentation, write a Python script that retrieves the 5 most recent finished ping measurements from the past year, where the probes used are located in Germany (country_code = "DE").

Steps:
- Use the /probes/ endpoint to get all connected German probes and extract their IDs into a list.
- Use the /measurements/ endpoint to get finished ping measurements from the past year (type="ping", af=4, status_name="Finished", start_time__gte=...).
- For each measurement, fetch results using /measurements/{id}/results/.
- In the results, check if any 'prb_id' matches a German probe ID. If yes, accept this measurement.
- Stop when 5 valid measurements are found.
- For each of those 5, extract all RTT values. RTTs may appear as result[].rtt or result[].result[].rtt. Handle both formats.
- Compute and print the average RTT per measurement.

Advice:
Always consult the provided documentation before writing the code. Especially regarding parameter names!
Avoid comparing probe IDs directly with measurement IDs. Use prb_id only from the results.
Ensure prb_id is compared correctly (it may be an integer in the results).
'objects' field does not exist, the correct one is 'results'.

Note:
Make sure to handle empty results gracefully and avoid errors with missing RTT values.

Output:
The script should print the Measurement ID and the average RTT for the 5 most recent valid measurements from probes located in Germany.
"""

import requests
from datetime import datetime, timedelta

# API Details
headers = {
    "Authorization": "Key 066fa78b-d292-463a-bc86-57a84c0d9399"
}
url_probes = "https://atlas.ripe.net/api/v2/probes/"
url_measurements = "https://atlas.ripe.net/api/v2/measurements/"

# Probe Filter Details
params_probe = {
    "status_name": "Connected",
    "country_code": "DE"
}

# Measurement Filter Details
end_time = int(datetime.now().timestamp())
start_time = end_time - 365*24*60*60
params_measurement = {
    "type": "ping",
    "af": 4,
    "status_name": "Finished",
    "start_time__gte": start_time,
    "end_time__lte": end_time
}


# Fetching German Probes
response = requests.get(url_probes, headers=headers, params=params_probe)
data_probes = response.json()["results"]
german_probe_ids = [str(probe['id']) for probe in data_probes]

# Fetching Finished Ping Measurements from the past year
response = requests.get(url_measurements, headers=headers, params=params_measurement)
data_measurements = response.json()["results"]

valid_measurements = []
for measurement in data_measurements:
    # Fetching Results for each Measurement
    params_results = {
        "format": "json",
        "_include-objects": "false"
    }
    url_results = f"{url_measurements}{measurement['id']}/results/"
    response = requests.get(url_results, headers=headers, params=params_results)
    data_results = response.json()
    
    # Checking if any German Probe ID matches with 'prb_id' in the results
    for result in data_results:
        try:
            prb_id = str(result['prb_id'])  # 'prb_id' may be an integer
        except KeyError:
            continue
        
        if prb_id in german_probe_ids and len(valid_measurements) < 5:
            valid_measurement = measurement
            
            try:    # RTT values are present at both 'result[].rtt' & 'result[].result[].rtt' 
                rtt = result['rtt']
            except KeyError:
                rtt = result['result']['rtt']
                
            valid_measurement['average_rtt'] = rtt
            valid_measurements.append(valid_measurement)
            
            break   # Next Measurement

# Printing the average RTT of the 5 most recent valid measurements from probes located in Germany
for measurement in valid_measurements:
    print("Measurement ID:", measurement['id'])
    print("Average RTT:", measurement['average_rtt'], "ms")


    """
    OUTPUT:

    File "/Users/matteotognetti/Desktop/uni/TESI/DeepSeek-coder/API:Chat/Test_3.py", line 60, in <module>
    rtt = result['rtt']
    KeyError: 'rtt'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
    File "/Users/matteotognetti/Desktop/uni/TESI/DeepSeek-coder/API:Chat/Test_3.py", line 62, in <module>
    rtt = result['result']['rtt']
    TypeError: list indices must be integers or slices, not str
    
    """