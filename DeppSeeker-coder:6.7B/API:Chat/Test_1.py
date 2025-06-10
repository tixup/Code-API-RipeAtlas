"""
PROMPT:

Write a Python 3 script using the requests library that queries the RIPE Atlas REST API v2. 
The goal is to retrieve the 5 most recent 'ping'-type measurements completed in the last 60 days. 
Format the results as a printed list with measurement ID and completion time in human-readable format.
Assume the API does not require authentication.

"""

import requests
from datetime import datetime, timedelta

# Calculate start and stop times for 60 days ago until now in UNIX timestamp format
now = int(datetime.utcnow().timestamp())
six_months_ago = int((datetime.utcnow() - timedelta(days=60)).timestamp())

params = {
    "type": "ping",
    "stop_time__lte": now,
    "start_time__gte": six_months_ago,
}

url = "https://atlas.ripe.net/api/v2/measurements/"
response = requests.get(url, params=params)
data = response.json()

# Sort the measurements based on completion time and take only the 5 most recent ones
sorted_results = sorted(data["results"], key=lambda x: x['stop_time'], reverse=True)[:5]

for result in sorted_results:
    # Convert UNIX timestamp to human-readable format
    completion_time = datetime.utcfromtimestamp(result["stop_time"]).strftime('%Y-%m-%d %H:%M:%S')
    
    print("Measurement ID: {}, Completion Time: {}".format(result['id'], completion_time))

"""
OUTPUT:

Measurement ID: 86736025, Completion Time: 2025-02-07 07:40:02
Measurement ID: 86736026, Completion Time: 2025-02-07 07:40:02
Measurement ID: 86736027, Completion Time: 2025-02-07 07:40:02
Measurement ID: 86736028, Completion Time: 2025-02-07 07:40:02
Measurement ID: 86736029, Completion Time: 2025-02-07 07:40:02

"""