"""
PROMPT:

Write a Python script to fetch and analyze RIPE Atlas ping measurements with these EXACT specifications:

1. API Requirements:
- Use v2 API endpoint: "https://atlas.ripe.net/api/v2/measurements/"
- Authentication: {'Authorization': 'Key YOUR_API_KEY'} (replace with actual key)
- Required parameters:
  * type='ping' (string)
  * status=2 (integer, completed measurements)
  * start_time__gte: UNIX timestamp (60 days ago)
  * stop_time__lte: UNIX timestamp (current time)
  * page_size=5 (integer)
  * format='json' (string)

2. Data Structure Clarifications (CRITICAL):
- Measurement object contains:
  * 'id': measurement ID (integer)
  * 'target_ip': direct string field (no nested 'target' object)
  * 'description': string
  * 'start_time': UNIX timestamp
- Results endpoint (/measurements/<ID>/results/) returns:
  * A LIST of probe result objects (not a dictionary with 'results' key)
  * Each probe result may contain:
    - Direct 'rtt' field (float) OR
    - 'result' dictionary containing 'rtt' (float)

3. Error-Prone Parts to Avoid:
- WRONG: measurement['target']['ip'] → CORRECT: measurement['target_ip']
- WRONG: response.json()['results'] → CORRECT: response.json() (already a list)
- Always check if 'rtt' exists before accessing it

4. Required Output:
For each measurement print:
Measurement ID: [id]
Target: [target_ip]
Description: [description]
Start: [ISO UTC time]
Avg Latency: [mean rtt or N/A]
Valid Probes: [count of probes with valid rtt]

5. Implementation Requirements:
- Use try/except blocks for all JSON parsing
- Handle missing fields gracefully
- Round average latency to 2 decimal places
- Include timeout=30 in all requests

Return ONLY the Python code wrapped in ```python ``` blocks.

Example of correct measurement object:
{
  "id": 12345,
  "target_ip": "8.8.8.8",
  "description": "Ping to Google DNS",
  "start_time": 1630000000
}

Example of correct probe result object:
{
  "prb_id": 123,
  "rtt": 12.34,
  "result": {"rtt": 12.34}  # Some have both!
}

"""

import requests
from datetime import datetime, timedelta

# Define the API endpoint and authentication header
api_endpoint = "https://atlas.ripe.net/api/v2/measurements/"
auth_header = {'Authorization': 'Key 066fa78b-d292-463a-bc86-57a84c0d9399'}

# Define the parameters for the API request
params = {
    'type': 'ping',
    'status': 2,
    'start_time__gte': (datetime.utcnow() - timedelta(days=60)).timestamp(),
    'stop_time__lte': datetime.utcnow().timestamp(),
    'page_size': 5,
    'format': 'json'
}

# Make the API request and get the response
response = requests.get(api_endpoint, headers=auth_header, params=params, timeout=30)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    measurements = response.json()["results"]

    # Iterate over the measurements and print the desired information
    for measurement in measurements:
        try:
            target_ip = measurement['target_ip']
            description = measurement['description']
            start_time = datetime.fromtimestamp(measurement['start_time'])
            avg_latency = None
            valid_probes = 0

            # Get the probe results for this measurement
            probe_results = requests.get(f'{api_endpoint}{measurement["id"]}/results/', headers=auth_header, timeout=30).json()

            # Iterate over the probe results and calculate the average latency
            for result in probe_results:
                try:
                    rtt = result['rtt']
                    avg_latency += rtt
                    valid_probes += 1
                except KeyError:
                    pass

            # Print the information for this measurement
            print(f'\nMeasurement ID: {measurement["id"]}')
            print(f'Target: {target_ip}')
            print(f'Description: {description}')
            print(f'Start: {start_time.isoformat()}')
            if avg_latency is not None:
                print(f'Avg Latency: {round(avg_latency / valid_probes, 2)} ms')
            else:
                print('Avg Latency: N/A')
            print(f'Valid Probes: {valid_probes}')
        except KeyError as e:
            print(f'Missing field in measurement {measurement["id"]}: {e}')


"""
OUTPUT:

Measurement ID: 87837406
Target: 200.12.26.11
Description: Ping measurement to emol.com
Start: 2025-02-27T10:46:45
Avg Latency: N/A
Valid Probes: 0

Measurement ID: 87850944
Target: 46.234.161.202
Description: Ping measurement to CEZ 46.234.161.202
Start: 2025-02-27T12:02:52
Avg Latency: N/A
Valid Probes: 0

Measurement ID: 88085138
Target: 9.9.9.9
Description: Nordic ping measurement to 9.9.9.9
Start: 2025-02-28T13:03:13
Avg Latency: N/A
Valid Probes: 0

...

(Anche qua problema sulla Latency e Valid Probes, non prende bene i valori in 'results')

"""