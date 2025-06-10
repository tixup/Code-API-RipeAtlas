"""
QUERY:

With the documentation I provided earlier, write a Python script that retrieves the 5 most recent finished ping measurements from the past year, where the probes used are located in Germany (country_code = "DE"). 
Use the RIPE Atlas API and my personal API key to authenticate.

Steps:
1. Use the `/probes/` endpoint to get all **currently connected** probes located in Germany. Extract their IDs into a list. Make sure to use the correct parameter for status (status_name="Connected") and use the field `results`, not `data` or `objects`.
2. Use the `/measurements/` endpoint to fetch **finished** ping measurements from the past year (type="ping", af=4, status_name="Finished", start_time__gte=...). The timestamp must be in **seconds**, not milliseconds.
3. For each measurement, use the `/measurements/{id}/results/` endpoint to retrieve its results.
4. In each result object, check if the `prb_id` is in the list of German probe IDs. If so, consider this measurement valid.
5. Stop once 5 valid measurements are found.
6. Print the Measurement ID and the matching German Probe ID.

Important:
- Use this API Key in the headers: `066fa78b-d292-463a-bc86-57a84c0d9399`
- Use only fields and parameter names that I have explained in the documentation.
- The correct response key is `results`, not `data` or `objects`.
- The `/results/` endpoint returns a **list**, not a dictionary.
- The probe ID (`prb_id`) must be compared as an integer, not a string.


"""

import requests
from datetime import datetime, timedelta

# Your personal API key
API_KEY = '066fa78b-d292-463a-bc86-57a84c0d9399'

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    'Authorization': f'Key {API_KEY}',
}

# Get all currently connected probes in Germany
response = requests.get('https://atlas.ripe.net/api/v2/probes/?format=json&status_name=Connected&country_code=DE', headers=headers)
data = response.json()['results']
probe_ids = [obj['id'] for obj in data]

# Get the timestamp of one year ago
one_year_ago = int((datetime.now() - timedelta(days=700)).timestamp())  # Convert to seconds

params = {
    'format': 'json',
    'type': 'ping',
    'af': 4,
    'status_name': 'Finished',
    'start_time__gte': one_year_ago,
}
# Fetch finished ping measurements from the past year
response = requests.get('https://atlas.ripe.net/api/v2/measurements/', headers=headers, params=params)
data = response.json()['results']

count = 0
for measurement in data:
    if count >= 5:
        break
        
    measurement_id = measurement['id']
    
    # Get the results of this specific measurement
    response = requests.get(f'https://atlas.ripe.net/api/v2/measurements/{measurement_id}/results/', headers=headers)
    data = response.json()
    
    for result in data:
        if int(result['prb_id']) in probe_ids:  # prb_id is a string, so we need to convert it to an integer first
            print(f'Measurement ID: {measurement_id}, German Probe ID: {result["prb_id"]}')
            count += 1
            break

"""
OUTPUT: (Dipende dall'intervallo di tempo selezionato + quante misurazioni in quella pagina, 'next' non viene usato)

Measurement ID: 69741971, German Probe ID: 2089
Measurement ID: 69742042, German Probe ID: 2707
Measurement ID: 69742053, German Probe ID: 2325
...

"""