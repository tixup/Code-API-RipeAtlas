"""
PROMPT:

Write a Python script that interacts with the RIPE Atlas public API to retrieve measurement data.
Here’s what the script should do:

1. Define a 60-day time window from the current UTC time (now) and convert the start and end time to Unix timestamps (in seconds). 
   Use the `datetime` module and `relativedelta` from `dateutil`.

2. Set up a GET request to the RIPE Atlas API endpoint:
   https://atlas.ripe.net/api/v2/measurements/
   Include the following parameters:
   - `type=ping`  → we only want ping measurements
   - `status=2`   → only retrieve completed measurements
   - `start_time__gte=<start_timestamp>`
   - `stop_time__lte=<end_timestamp>`
   - `page_size=5` to limit the result set to 5 measurements
   - `format=json`

3. The request requires an API key passed as a header. Set the header:
   `'Authorization': 'Key <YOUR_API_KEY>'`

4. Parse the JSON response, check that the top-level key 'results' is present, and extract the list of measurements.

5. For each measurement, extract:
   - the measurement ID (`id`)
   - the target IP address (`target_ip`)
   - the description (`description`)
   - the start time (`start_time` → convert it from Unix timestamp to UTC ISO format)

6. Then make another GET request to:
   https://atlas.ripe.net/api/v2/measurements/<ID>/results/
   Replace `<ID>` with the actual measurement ID.
   This endpoint returns a list (not a dictionary!) containing probe results.

7. Parse and store the probe results from the second request. Calculate the average latency for each measurement as follows:
   - Extract all 'rtt' values (in milliseconds) from the 'result' field of each probe result (a list of dictionaries).
   - Compute the mean of all 'rtt' values across all probes for that measurement, ignoring entries without 'rtt' (e.g., errors or timeouts).
   - If no valid 'rtt' values are found, set the average latency to 'N/A'.

8. Print a readable summary for each measurement as follows:
   - Measurement ID
   - Target IP
   - Description
   - Start time (in UTC ISO format)
   - Average Latency (in milliseconds, rounded to 2 decimal places, or 'N/A' if not calculable)

Use the `requests` library for HTTP calls and handle any response errors or JSON decoding issues. Add comments in the code to clearly show each step. The goal is to have a working script that pulls basic measurement data from RIPE Atlas and includes the average latency for each measurement.

"""


import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json

# Define start and end times for a 60-day window from now
end_time = datetime.utcnow()
start_time = end_time - relativedelta(days=60)

start_timestamp = int(start_time.strftime('%s'))
end_timestamp = int(end_time.strftime('%s'))

# Build GET request URL and headers
url = f"https://atlas.ripe.net/api/v2/measurements/?type=ping&status=2&start_time__gte={start_timestamp}&stop_time__lte={end_timestamp}&page_size=5&format=json"
headers = {'Authorization': f'Key 066fa78b-d292-463a-bc86-57a84c0d9399'}

# Send GET request to RIPE Atlas API
response = requests.get(url, headers=headers)

# Check if the response was successful
if not response.ok:
    print('Failed to get data from RIPE Atlas API:', response.status_code)
else:
    # Parse JSON data
    try:
        measurements = json.loads(response.text)['results']
        
        for measurement in measurements:
            # Get measurement details and send another GET request to fetch results
            id = measurement['id']
            target_ip = measurement['target_ip']
            description = measurement['description']
            start_time = datetime.utcfromtimestamp(measurement['start_time']).isoformat()
            
            response = requests.get(f"https://atlas.ripe.net/api/v2/measurements/{id}/results/?format=json", headers=headers)
            
            # Check if the results retrieval was successful
            if not response.ok:
                print('Failed to get result data from RIPE Atlas API:', response.status_code)
                average_latency = 'N/A'
            else:
                # Parse probe results and calculate average latency
                try: 
                    rtts = [result['rtt'] for result in json.loads(response.text)]
                    average_latency = sum([int(rtt) for rtt in rtts if rtt is not None]) / len(rtts)
                    average_latency = round(average_latency, 2)
                except (KeyError, ValueError):
                    # Couldn't calculate average latency
                    average_latency = 'N/A'
            
            # Print measurement summary
            print('\nMeasurement ID:', id)
            print('Target IP:', target_ip)
            print('Description:', description)
            print('Start time:', start_time)
            print('Average Latency (ms):', average_latency)
            
    except (KeyError, json.JSONDecodeError) as e:
        # Couldn't parse response data
        print(f"Failed to decode JSON: {str(e)}")


"""
OUTPUT: (Dipende dall'intervallo di tempo)

Measurement ID: 91131482
Target IP: 34.72.205.31
Description: Ping measurement to 34.72.205.31
Start time: 2025-03-12T22:50:00
Average Latency (ms): N/A

Measurement ID: 91440973
Target IP: 158.181.55.142
Description: Ping measurement to 158.181.55.142
Start time: 2025-03-14T14:13:00
Average Latency (ms): N/A

...


Problema su Avarage Latency, non riesce a prelevare i campioni 'rtt': 

* Struttura dei dati più complessa:
{
  "result": [{"rtt": 1.56}, {"rtt": 4.42}],  // Array di tentativi
  "rcvd": 3,                                 // Pacchetti ricevuti
  "avg": 2.49                                // Media precalcolata
}

* Estrazione dei campi errata:

# SBAGLIATO (nel Codice Test_3.py):
rtts = [result['rtt'] for result in json.loads(response.text)]

# CORRETTO (preso da codice funzionante FINAL_NO_COUNTRY.py):
rtts = [ping['rtt'] for result in json.loads(response.text) 
        for ping in result.get('result', []) 
        if isinstance(ping.get('rtt'), (int, float))]


"""