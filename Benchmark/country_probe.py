def get_german_probes():
    """Recupera tutti i probe tedeschi connessi con gestione errori"""
    try:
        params = {
            "country_code": "DE",
            "status": 1,  # Connected
            "fields": "id",
            "limit": 200  # Limite aumentato
        }
        response = requests.get(f"{BASE_URL}probes/", headers=headers, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return {probe["id"] for probe in response.json()["results"]}
    except Exception as e:
        print(f"Errore recupero probe tedeschi: {str(e)}")
        return set()