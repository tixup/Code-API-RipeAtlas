
""" 
PROMPT: 

Write a Python script that queries the RIPE Atlas REST API to retrieve the last 5 ping-type measurements completed in the last 60 days.

For each measurement, the script must:
1. Send a GET request to the RIPE Atlas API endpoint:
   https://atlas.ripe.net/api/v2/measurements/, using appropriate query parameters such as type, status ('2'), page_size ('5'), start and end time in the last 60 days.
2. Define a 60-day time window from the current UTC time (now) and convert start and end times to Unix timestamps (in seconds). 
3. Print the measurement ID, target IP (target_ip), description (description), and start time in UTC ISO format.

The RIPE Atlas API requires authentication using an API key. Set the Authorization header to: Key <your_token>.

Add basic error handling for failed HTTP responses or unexpected data.

"""

import requests
from datetime import datetime, timedelta

# Define start and end time for 60 days ago
end_time = int(datetime.utcnow().timestamp())
start_time = int((datetime.utcnow() - timedelta(days=60)).timestamp())

headers = {
    'Authorization': 'Key 066fa78b-d292-463a-bc86-57a84c0d9399',
}

params = {
    "type": "ping", 
    "status": "2",   # status 2 means completed
    "page_size": "5", 
    "start_time__gte": start_time, 
    "end_time__lte": end_time
}

try:
    response = requests.get('https://atlas.ripe.net/api/v2/measurements/', headers=headers, params=params)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status() 
    
    data = response.json().get("results")  
     
    for measurement in data:
        print(f"Measurement ID: {measurement['id']}, Target IP: {measurement['target_ip']}, Description: {measurement['description']}, Start Time: {datetime.fromtimestamp(int(measurement['start_time'])).strftime('%Y-%m-%d %H:%M:%S')}")
        
except requests.HTTPError as errh:
    print ("Http Error:",errh)
except requests.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.Timeout as errt:
    print ("Timeout Error:",errt)
except requests.RequestException as errr:
    print ("Something went wrong with the request: ",errr)


"""
OUTPUT:

Measurement ID: 85962105, Target IP: 5.32.229.249, Description: Ping measurement to 5.32.229.249 (Probe 50309 - Oman) - LWV2, Start Time: 2025-03-08 22:00:00
Measurement ID: 86718422, Target IP: 2a01:239:2a6:d500::1, Description: IPv6 ping to vps-de.orleans.ddnss.de, Start Time: 2025-02-06 17:31:55
Measurement ID: 86727360, Target IP: 2606:4700:7000::6715:f409, Description: Ping measurement to invalid.rpki.cloudflare.com, Start Time: 2025-02-07 00:25:00
Measurement ID: 86731256, Target IP: 207.211.162.92, Description: Ping measurement to ordvmb.shanesvcn.net, Start Time: 2025-02-07 03:18:40
Measurement ID: 86741434, Target IP: 183.177.253.175, Description: Ping measurement to 183.177.253.175, Start Time: 2025-02-07 13:44:00

"""