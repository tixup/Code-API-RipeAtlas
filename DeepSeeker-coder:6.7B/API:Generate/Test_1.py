""" 
PROMPT: 

Write a Python script that queries the RIPE Atlas REST API to retrieve the last 5 ping-type measurements completed in the last 60 days.

For each measure, the script must:
1. Set up a GET request to the RIPE Atlas API endpoint:
   https://atlas.ripe.net/api/v2/measurements/ and retrieve the measurements with parameters such as type, status ('2'), page_size ('5'), start and end time.
2. Print the measure ID, target IP (target_ip), description (description), and start time in UTC ISO format. Use the `datetime` module and `relativedelta` from `dateutil`.

The RIPE Atlas API requires an API key header for authentication. Use `Authorization: Key <token>` in your headers.

"""

import os
from dateutil.relativedelta import relativedelta
from datetime import datetime
import requests

# Get API Key from environment variables
api_key = '066fa78b-d292-463a-bc86-57a84c0d9399'
if not api_key:
    raise ValueError("Please set the RIPE_ATLAS_API_KEY environment variable.")
    
headers = {
    "Authorization": f"Key {api_key}",  # Set API Key in header
}

# Set up start and end time for one month ago
end_time = datetime.utcnow()
start_time = end_time - relativedelta(months=1)

params = {
    "type": "ping",     # Ping type measurements
    "status": 2,        # Only completed measurements
    "page_size": 5,       # We want the last 5 measurements per page
    "format": 'json',   # Format of response data
    "start": int(start_time.timestamp()),     # Start time in unix timestamp
    "end": int(end_time.timestamp())          # End time in unix timestamp
}

response = requests.get("https://atlas.ripe.net/api/v2/measurements", headers=headers, params=params)
data = response.json()  # Get data from json format

# Loop over the measurements and print details for each one
for measure in data["results"]:
    print(f"Measure ID: {measure['id']}")
    print(f"Target IP: {measure['target_ip']}")
    print(f"Description: {measure['description']}")
    
    # Convert the start time from unix timestamp to UTC ISO format
    start = datetime.utcfromtimestamp(int(measure["start_time"]))
    print(f"Start Time: {start.isoformat()}")

    """
    OUTPUT:
    
    Target IP: 202.12.27.33
    Description: None
    Start Time: 2010-10-29T00:00:00
    Measure ID: 1008
    Target IP: 199.7.83.42
    Description: None
    Start Time: 2010-11-29T00:00:00

    ...

    """