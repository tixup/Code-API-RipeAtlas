"""
PROMPT:

Write a Python script using RIPE Atlas API passed before, that retrieves and displays the 5 most recent completed ping measurements from German probes. The script must:

1. FOLLOW THIS EXACT WORKFLOW:
   a) FIRST fetch all currently connected German probes (status=1)
   b) THEN get recent finished ping measurements (status=2)
   c) FINALLY verify which measurements used German probes

2. CRITICAL FIXES NEEDED:
   - properly handle the "/results/" endpoint response (it returns a LIST)
   - check ALL results in the list for German probes
   - use the correct parameter names (status=1/2, not status_name)
   - convert timestamps to UNIX seconds (integer)
   - verify response.ok before processing

3. API ENDPOINT SPECIFICS:
   - /probes/:
     * Parameters: country_code="DE", status=1, fields="id"
     * Response contains "results" list with "id" field
   
   - /measurements/:
     * Parameters: type="ping", af=4, status=2
     * MUST include: start_time__gte=(now-365 days) in UNIX seconds
     * MUST sort by "-start_time" (most recent first)
   
   - /measurements/{id}/results/:
     * Returns a LIST of result objects
     * Each result has "prb_id" field (convert to int)

4. ERROR HANDLING:
   - Verify response.ok for every request
   - Print descriptive error messages
   - Skip failed requests (don't exit)
   - Handle empty responses gracefully

5. OUTPUT REQUIREMENTS:
   - Print exactly 5 valid measurements
   - Format: "Measurement {id} with German probe {prb_id}"
   - Include progress messages

6. TECHNICAL DETAILS:
   API_KEY = "066fa78b-d292-463a-bc86-57a84c0d9399"
   BASE_URL = "https://atlas.ripe.net/api/v2/"
   Headers = {
       "Authorization": f"Key {API_KEY}",
       "Accept": "application/json"
   }

Required structure:
1. Get German probe IDs (set)
2. Get recent measurements (sorted by date)
3. For each measurement, get ALL results
4. Check each result for German probes
5. Print first 5 matches

PROHIBITED MISTAKES:
- Never assume single result per measurement
- Never forget to convert prb_id to int
- Never process more than 5 valid measurements
- Never use string concatenation for URLs (use params)
- Never forget to check response status

LIBRARIES:
- requests, datetime.timedelta

"""
import requests
from datetime import datetime, timedelta

# API endpoint URLs
BASE_URL = "https://atlas.ripe.net/api/v2/"
PROBES_ENDPOINT = f"{BASE_URL}probes/"
MEASUREMENTS_ENDPOINT = f"{BASE_URL}measurements/"

# API parameters and headers
API_KEY = "066fa78b-d292-463a-bc86-57a84c0d9399"
HEADERS = {
    "Authorization": f"Key {API_KEY}",
    "Accept": "application/json"
}

def get_german_probe_ids():
    # Fetch all currently connected German probes (status=1)
    params = {
        "country_code": "DE",
        "status": 1,
        "fields": "id"
    }
    response = requests.get(PROBES_ENDPOINT, headers=HEADERS, params=params)
    if not response.ok:
        print(f"Error fetching German probes: {response.text}")
        return None
    results = response.json()["results"]
    probe_ids = set()
    for result in results:
        probe_ids.add(int(result["id"]))
    return probe_ids

def get_recent_measurements():
    # Get recent finished ping measurements (status=2)
    params = {
        "type": "ping",
        "af": 4,
        "status": 2,
        "start_time__gte": int((datetime.now() - timedelta(days=365)).timestamp()),
        "sort": "-start_time"
    }
    response = requests.get(MEASUREMENTS_ENDPOINT, headers=HEADERS, params=params)
    if not response.ok:
        print(f"Error fetching recent measurements: {response.text}")
        return None
    results = response.json()["results"]
    return results

def get_measurement_results(measurement_id):
    # Get all results for a measurement
    params = {
        "type": "ping",
        "af": 4,
        "status": 2,
        "start_time__gte": int((datetime.now() - timedelta(days=365)).timestamp()),
        "sort": "-start_time"
    }
    response = requests.get(f"{MEASUREMENTS_ENDPOINT}{measurement_id}/results/", headers=HEADERS, params=params)
    if not response.ok:
        print(f"Error fetching measurement results: {response.text}")
        return None
    results = response.json()["results"]
    return results

def check_for_german_probes(measurement_id):
    # Check each result for German probes
    results = get_measurement_results(measurement_id)
    if not results:
        print("No results found for measurement")
        return False
    german_probe_ids = get_german_probe_ids()
    if not german_probe_ids:
        print("No German probes found")
        return False
    for result in results:
        prb_id = int(result["prb_id"])
        if prb_id in german_probe_ids:
            # Found a match! Print it and break out of the loop.
            print(f"Measurement {measurement_id} with German probe {prb_id}")
            return True
    # No matches found.
    return False

if __name__ == "__main__":
    # Get all currently connected German probes (status=1)
    german_probe_ids = get_german_probe_ids()
    if not german_probe_ids:
        print("No German probes found")
        exit(0)

    # Get recent finished ping measurements (status=2)
    recent_measurements = get_recent_measurements()
    if not recent_measurements:
        print("No recent measurements found")
        exit(0)

    # For each measurement, get ALL results and check for German probes
    count = 0
    for measurement in recent_measurements:
        measurement_id = int(measurement["id"])
        if check_for_german_probes(measurement_id):
            count += 1
        # Exit after printing 5 valid measurements
        if count == 5:
            break
    print(f"Found {count} valid measurements with German probes")

    """
    OUTPUT:

    TypeError: list indices must be integers or slices, not str

    Commenti:
    Causa Errore: L'endpoint /results/ restituisce direttamente una lista, non un dizionario con chiave "results".
    get_measurement_results(): Tentativo di accedere a response.json()["results"] quando l'API restituisce direttamente la lista.
    check_for_german_probes(): Non gestisce il caso in cui prb_id non esista nel risultato, stampa direttamente invece di restituire i risultati

    """