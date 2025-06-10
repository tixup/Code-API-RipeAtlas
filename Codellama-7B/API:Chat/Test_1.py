"""
QUERY:

Write a Python 3 script using the requests library that queries the RIPE Atlas REST API v2. 
The goal is to retrieve the 5 most recent 'ping'-type measurements completed in the last 60 days. 
Format the results as a printed list with measurement ID and completion time in human-readable format.
Assume the API does not require authentication. 

"""


import requests
from datetime import datetime, timedelta

# Set the target URL and query parameters
url = "https://atlas.ripe.net/api/v2/measurements/"
params = {
    "type": "ping",
    "start_time__gte": (datetime.now() - timedelta(days=60)).timestamp(),
    "stop_time__lte": datetime.now().timestamp(),
}

# Set the headers
headers = {"Authorization": "Key 066fa78b-d292-463a-bc86-57a84c0d9399"}

# Send a GET request to the API and read the response as JSON
response = requests.get(url, headers=headers, params=params)
data = response.json()

# Print the results in a list format
print("Top 5 most recent ping measurements:")
for i, measurement in enumerate(data["results"][:5]):
    print(f"{i+1}. {measurement['id']} - {datetime.fromtimestamp(measurement['stop_time']).strftime('%Y-%m-%d %H:%M:%S')}")

"""
OUTPUT:

Top 5 most recent ping measurements:
1. 85962105 - 2025-04-08 23:00:00
2. 86804638 - 2025-02-09 14:40:02
3. 86804639 - 2025-02-09 14:40:02
4. 86804640 - 2025-02-09 14:40:02
5. 86804641 - 2025-02-09 14:40:02

"""