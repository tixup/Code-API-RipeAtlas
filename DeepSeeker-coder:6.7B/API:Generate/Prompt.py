import requests

prompt = """  
Write a Python script to fetch and analyze RIPE Atlas ping measurements with these EXACT specifications:

1. API Requirements:
- Base endpoint: "https://atlas.ripe.net/api/v2/measurements/"
- Authentication: {'Authorization': 'Key YOUR_API_KEY'}
- Timeout: 30 seconds for all requests

2. Data Structure (CRITICAL):
- Measurements list (GET /measurements/):
  [
    {
      "id": 12345,
      "target_ip": "8.8.8.8",
      "description": "Ping measurement",
      "start_time": 1630000000
    }
  ]

- Probe results (GET /measurements/<ID>/results/):
  [
    {
      "result": [{"rtt": 1.5}, {"rtt": 2.3}],  // List of pings
      "rcvd": 2,                               // Packets received
      "sent": 3,                               // Packets sent
      "avg": 1.9,                              // Pre-calculated average
      "msm_id": 12345,                         // Measurement ID
      "prb_id": 67890,                         // Probe ID
      "timestamp": 1630000000                  // Measurement time
    }
  ]

3. Implementation Rules:
- For EACH measurement:
  a) First fetch basic info from /measurements/
  b) Then fetch detailed results from /measurements/<ID>/results/
  
- Calculate latency by:
  1. Prefer using 'avg' field when available
  2. Fallback to calculating mean from 'result' array
  3. Filter invalid RTTs (<=0 or >=1000)

- Calculate success rate: (rcvd/sent)*100

4. Error Handling (MUST INCLUDE):
- Check response.status_code == 200
- Verify JSON structure at each step
- Handle missing fields with .get()
- Skip corrupted measurements

5. Output Format:
Measurement ID: [id]
Target: [target_ip]
Start: [ISO UTC time]
Avg Latency: [value] ms
Success Rate: [value]%
Valid Probes: [count]

6. Special Cases:
- If no valid RTTs: show "N/A" for latency
- If sent=0: show 0% success rate
- If timestamp missing: show "N/A"

Return ONLY the Python code wrapped in ```python ``` blocks.
"""

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "deepseek-coder:6.7b",
    "prompt": prompt,
    "stream": False
})

print(response.json()["response"])
