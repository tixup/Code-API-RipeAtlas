def analyze_latency(measurement_id):
    """Analisi ottimizzata della latenza"""
    try:
        url = f"{BASE_URL}measurements/{measurement_id}/results/?limit=1000"  # Piu' risultati
        response = requests.get(url, headers={"Authorization": f"Key {API_KEY}"}, timeout=60)
        results = response.json()
        
        latencies = []
        for r in results:
            if isinstance(r, dict):
                if isinstance(r.get('rtt'), (int, float)) and 0 < r['rtt'] < 1000:
                    latencies.append(r['rtt'])
                elif isinstance(r.get('result'), list):
                    for ping in r['result']:
                        if isinstance(ping.get('rtt'), (int, float)) and 0 < ping['rtt'] < 1000:
                            latencies.append(ping['rtt'])
        
        if not latencies or len(latencies) < 100:  # Minimo 100 campioni
            return None
            
        return {
            'avg': statistics.mean(latencies),
            'median': statistics.median(latencies),
            'min': min(latencies),
            'max': max(latencies),
            'samples': len(latencies)
        }
        
    except Exception as e:
        print(f"Errore analisi: {str(e)}")
        return None