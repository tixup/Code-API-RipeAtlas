import requests

prompt = """

Write a Python script to fetch and analyze RIPE Atlas ping measurements with these EXACT specifications:

1. API Requirements:
- Use v2 API endpoint: "https://atlas.ripe.net/api/v2/measurements/"
- Use authentication header: {'Authorization': 'Key YOUR_API_KEY'}
- Required GET parameters:
  * type='ping'
  * status=2 (completed measurements)
  * start_time__gte: UNIX timestamp (60 days ago)
  * stop_time__lte: UNIX timestamp (now)
  * page_size=5
  * format='json'

2. Parse the JSON response, extracting measurements from the 'results' field. extract:
  * 'id'
  * 'target_ip'
  * 'description'
  * 'start_time' (convert to ISO UTC)

3. For each measurement, fetch results from:
  - `https://atlas.ripe.net/api/v2/measurements/<ID>/results/`
  - Each item in this list is a probe result, containing:
    * 'result': a list of ping attempts (each with 'rtt')
    * 'rcvd': number of successful pings
    * 'sent': number of pings attempted
    * 'avg': average RTT (optional)

4. For each probe:
  - Use 'avg' if available
  - Else compute average from 'rtt' values in 'result'
  - Skip probes where 'rcvd' is 0 or 'result' is empty

5. For each measurement, compute:
  - Global average latency: mean of valid probe averages
  - Overall success rate: total_rcvd / total_sent (sum over all probes)

6. Print for each measurement:
Measurement ID: [id]  
Target: [target_ip]  
Description: [description]  
Start: [ISO UTC time]  
Avg Latency: [value] ms  
Success Rate: [rcvd/sent]%

7. Handle errors:
- Set timeout=30 for all requests
- Check status_code == 200
- Wrap JSON parsing and field access in try/except
- Skip measurements or probes with missing data

Example of '/measurements/<id>/results/' result object:
{
  "result": [{"rtt": 1.5}, {"rtt": 2.3}],
  "rcvd": 2,
  "sent": 3,
  "avg": 1.9,
  "msm_id": 12345,
  "prb_id": 67890
}

Return ONLY the Python code wrapped in ```python ``` blocks.

"""


response = requests.post("http://localhost:11434/api/generate", json={
    "model": "codellama",
    "prompt": prompt,
    "stream": False
})

print(response.json()["response"])