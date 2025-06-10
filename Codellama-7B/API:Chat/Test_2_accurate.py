"""
QUERY:

With the provided documentation, write a Python script that retrieves the 5 most recent finished ping measurements from the past year, where the probes used are located in Germany (country_code = "DE").

Steps:
- Use the /probes/ endpoint to get all connected German probes and extract their IDs into a list.
- Use the /measurements/ endpoint to get finished ping measurements from the past year (type="ping", af=4, status_name="Finished", start_time__gte=...).
- For each measurement, fetch results using /measurements/{id}/results/.
- In the results, check if any 'prb_id' matches a German probe ID. If yes, accept this measurement.
- Stop when 5 valid measurements are found.
- For each of those 5, extract all RTT values. RTTs may appear as result[].rtt or result[].result[].rtt. Handle both formats.
- Compute and print the average RTT per measurement.

Advice:
Always consult the provided documentation before writing the code. Especially regarding parameter names!
Avoid comparing probe IDs directly with measurement IDs. Use prb_id only from the results.
Ensure prb_id is compared correctly (it may be an integer in the results).
'objects' field does not exist, the correct one is 'results'.

Note:
Make sure to handle empty results gracefully and avoid errors with missing RTT values.

Output:
The script should print the Measurement ID and the average RTT for the 5 most recent valid measurements from probes located in Germany.

"""


import requests

def get_german_probes():
    url = "https://atlas.ripe.net/api/v2/probes/"
    headers = {
        "Authorization": "Key 066fa78b-d292-463a-bc86-57a84c0d9399"
    }
    params = {
        "country_code": "DE",
        "status": "Connected",
        "public": "True"
    }
    response = requests.get(url, headers=headers, params=params)
    probes = []
    for probe in response.json()["objects"]:
        if probe["country_code"] == "DE":
            probes.append(probe["id"])
    return probes

def get_measurements(probes, start_time):
    url = "https://atlas.ripe.net/api/v2/measurements/"
    headers = {
        "Authorization": "Key 066fa78b-d292-463a-bc86-57a84c0d9399"
    }
    params = {
        "type": "ping",
        "af": 4,
        "status_name": "Finished",
        "start_time__gte": start_time
    }
    response = requests.get(url, headers=headers, params=params)
    measurements = []
    for measurement in response.json()["objects"]:
        if measurement["probe_ids"][0] in probes:
            measurements.append(measurement)
    return measurements

def get_rtts(measurements):
    rtts = []
    for measurement in measurements:
        url = f"https://atlas.ripe.net/api/v2/measurements/{measurement['id']}/results/"
        response = requests.get(url, headers={"Authorization": "Key 066fa78b-d292-463a-bc86-57a84c0d9399"})
        for result in response.json()["objects"]:
            if isinstance(result, dict):
                if "rtt" in result:
                    rtts.append(result["rtt"])
            elif isinstance(result, list):
                for sub_result in result:
                    if "rtt" in sub_result:
                        rtts.append(sub_result["rtt"])
    return rtts

if __name__ == "__main__":
    probes = get_german_probes()
    measurements = get_measurements(probes, "2022-01-01T00:00:00")
    print("Measurement ID\tAverage RTT")
    for measurement in measurements[:5]:
        rtts = get_rtts([measurement])
        average_rtt = sum(rtts) / len(rtts)
        print(f"{measurement['id']}\t{average_rtt}")


"""
OUTPUT:

for probe in response.json()["results"]:
KeyError: 'results'

"""