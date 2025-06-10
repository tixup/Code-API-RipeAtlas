"""
QUERY:

With the documentation I provided earlier, write a Python script that retrieves the 5 most recent finished ping measurements from the past year, where the probes used are located in Germany (country_code = "DE"). 
Use the RIPE Atlas API and my personal API key to authenticate. Use library 'requests' , 'datetime' and 'timedelta'.

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

# API Key
api_key = "066fa78b-d292-463a-bc86-57a84c0d9399"

# Set up headers with the API key
headers = {
    'Authorization': f'Key {api_key}'
}

# Set up the params for the probes endpoint
probes_params = {
    'status_name': "Connected",
    'country_code': "DE"
}

# Set up the params for the measurements endpoint
measurements_params = {
    'type': "ping",
    'af': 4,
    'status_name': "Finished",
    'start_time__gte': datetime.now() - timedelta(days=365),
}

# Make the requests to the endpoints
probes_response = requests.get("https://atlas.ripe.net/api/v2/probes", headers=headers, params=probes_params)
measurements_response = requests.get("https://atlas.ripe.net/api/v2/measurements", headers=headers, params=measurements_params)

# Extract the list of German probe IDs from the probes response
german_probes = [probe['id'] for probe in probes_response.json()['results']]

# Initialize a counter for the number of valid measurements found
valid_measurements = 0

# Iterate over the measurements and check if the prb_id is in the list of German probes
for measurement in measurements_response.json()['results']:
    if measurement['prb_id'] in german_probes:
        valid_measurements += 1
        if valid_measurements == 5:
            # Print the Measurement ID and the matching German Probe ID
            print(f"Measurement {measurement['id']} with German probe {measurement['prb_id']}")
            break


"""
OUTPUT:

for measurement in measurements_response.json()['results']:
KeyError: 'results'

altri errori:
- non converte la data in timestap UNIX in secondi
- dovrebbe fare una richiesta separata per i risultati di ogni misurazione 
(Prima si ottiene la lista delle misurazioni, poi per ogni misurazione si ottengono i risultati separatamente, poi si verifica ogni risultato per i probe tedeschi)

"""