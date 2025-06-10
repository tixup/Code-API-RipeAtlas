"""
QUERY:

Write a Python script that uses the RIPE Atlas API to:

1. Fetch all currently connected German probes from `/api/v2/probes/` using `country_code=DE` and `status_name=Connected`. Store their `id`s in a list. Print them.

2. Fetch ping measurements from `/api/v2/measurements/` with:
   - `type=ping`
   - `status_name=Finished`
   - `start_time__gte` = UNIX timestamp for one year ago.
   Only fetch **up to 3 pages** using the `next` field in the JSON response.

3. For each measurement, request its results using `/api/v2/measurements/{id}/results/`.
   This endpoint returns a **list of dicts**, NOT a dict with a `'results'` key.

4. If any result contains a `prb_id` that matches a German probe, store the `measurement_id` and `prb_id`.

5. Stop after collecting 5 such measurements. Print:  
   `Measurement ID: <id>, German Probe ID: <prb_id>`

Important:
- Use your own API key with the header `"Authorization": "Key <API_KEY>"`.
- Avoid hardcoding any probe IDs.
- Carefully check the structure of the API responses.
- Do not assume all responses contain expected fields. Handle errors and type mismatches.

"""


import requests
from datetime import datetime, timedelta

# 1. Fetch German connected probes
url = "https://atlas.ripe.net/api/v2/probes/"
headers = {
    "Authorization": "Key 066fa78b-d292-463a-bc86-57a84c0d9399" # Replace with your key
}
params = {
    "country_code":"DE", 
    "status_name":"Connected"
}
response = requests.get(url, headers=headers, params=params)
data = response.json()
connected_probes = [probe['id'] for probe in data['results']]
print("Connected German Probes: ", connected_probes)

# 2. Fetch ping measurements
one_year_ago = int((datetime.now() - timedelta(days=365)).timestamp()) # UNIX timestamp for one year ago
url = "https://atlas.ripe.net/api/v2/measurements/"
params = {
    "type":"ping", 
    "status_name":"Finished", 
    "start_time__gte": one_year_ago, # Fetch measurements starting from one year ago
}
response = requests.get(url, headers=headers, params=params)
data = response.json()

# 3 & 4. Store and print relevant data
stored = 0
for measurement in data['results']:
    # Fetch results for each measurement
    url_results = f"https://atlas.ripe.net/api/v2/measurements/{measurement['id']}/results/"
    response = requests.get(url_results, headers=headers)
    data_results = response.json()
    
    for result in data_results: # data_results is a list of dicts, not a single dict with 'results' key
        if 'prb_id' in result and result['prb_id'] in connected_probes:  
            print(f"Measurement ID: {measurement['id']}, German Probe ID: {result['prb_id']}")
            stored += 1
    # Stop after collecting 5 such measurements. 
    if stored >= 5:
        break

# Check for errors in responses
if 'errors' in data or ('next' in data and requests.get(data['next']).status_code != 200):  
    print("Error occurred")


    """
    OUTPUT:

    Connected German Probes:  [46, 67, 80, 81, 137, 159, 164, 211, 233, 274, 277, 325, 382, 407, 560, 706, 756, 823, 901, 910, 916, 968, 975, 1206, 1212, 1280, 1312, 1313, 1326, 1330, 1336, 1338, 1343, 1350, 1359, 1370, 1388, 1415, 1458, 1463, 1472, 1485, 1497, 1506, 1509, 2024, 2052, 2057, 2074, 2081, 2089, 2097, 2098, 2108, 2147, 2153, 2168, 2176, 2205, 2208, 2227, 2229, 2237, 2275, 2290, 2302, 2303, 2322, 2325, 2326, 2332, 2364, 2383, 2430, 2434, 2453, 2468, 2477, 2478, 2615, 2626, 2631, 2632, 2650, 2662, 2707, 2715, 2739, 2750, 2777, 2809, 2867, 2920, 2934, 2941, 2960, 3017, 3068, 3112, 3150]
    Measurement ID: 69743539, German Probe ID: 3112
    Measurement ID: 69743540, German Probe ID: 2707
    Measurement ID: 69743540, German Probe ID: 823
    Measurement ID: 69743548, German Probe ID: 2707
    Measurement ID: 69743548, German Probe ID: 823

    """